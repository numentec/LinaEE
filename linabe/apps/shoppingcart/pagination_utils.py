"""
Utilidades para paginación en memoria de stored procedures externos.

Para casos donde el stored procedure devuelve todos los registros
y necesitamos paginar en el lado de Python.
"""

from rest_framework.utils.urls import replace_query_param, remove_query_param


class InMemoryPaginator:
    """
    Paginador en memoria para resultados de stored procedures.
    Optimizado para bases de datos que no soportan OFFSET/LIMIT.
    """
    
    def __init__(self, page_size=20, max_page_size=1000):
        self.page_size = page_size
        self.max_page_size = max_page_size
        
    def paginate_data(self, data, request):
        """
        Pagina una lista de datos en memoria.
        
        Args:
            data (list): Lista completa de resultados del stored procedure
            request: Request de Django REST Framework
            
        Returns:
            dict: Respuesta paginada con metadatos
        """
        if not data:
            return self._empty_response()
        
        # Obtener parámetros de paginación
        page = self._get_page_number(request)
        page_size = self._get_page_size(request)
        
        # Calcular paginación
        total_count = len(data)
        total_pages = (total_count + page_size - 1) // page_size
        
        # Validar página
        if page > total_pages:
            page = total_pages
        if page < 1:
            page = 1
            
        # Extraer datos de la página actual
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        page_data = data[start_index:end_index]
        
        # Construir URLs de navegación
        next_url = self._get_next_url(request, page, total_pages)
        previous_url = self._get_previous_url(request, page)
        
        return {
            'count': total_count,
            'next': next_url,
            'previous': previous_url,
            'results': page_data,
            'page_info': {
                'current_page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_previous': page > 1,
                'start_index': start_index + 1,  # 1-indexed para display
                'end_index': min(end_index, total_count)
            }
        }
    
    def _get_page_number(self, request):
        """Extrae el número de página de los query parameters."""
        try:
            page = int(request.query_params.get('page', 1))
            return max(1, page)  # Asegurar que sea al menos 1
        except (TypeError, ValueError):
            return 1
    
    def _get_page_size(self, request):
        """Extrae el tamaño de página de los query parameters."""
        try:
            page_size = int(request.query_params.get('page_size', self.page_size))
            return min(max(1, page_size), self.max_page_size)  # Entre 1 y max_page_size
        except (TypeError, ValueError):
            return self.page_size
    
    def _get_next_url(self, request, current_page, total_pages):
        """Construye la URL para la página siguiente."""
        if current_page >= total_pages:
            return None
        
        url = request.build_absolute_uri()
        return replace_query_param(url, 'page', current_page + 1)
    
    def _get_previous_url(self, request, current_page):
        """Construye la URL para la página anterior."""
        if current_page <= 1:
            return None
        
        url = request.build_absolute_uri()
        if current_page == 2:
            return remove_query_param(url, 'page')
        return replace_query_param(url, 'page', current_page - 1)
    
    def _empty_response(self):
        """Respuesta para cuando no hay datos."""
        return {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
            'page_info': {
                'current_page': 1,
                'page_size': self.page_size,
                'total_pages': 0,
                'has_next': False,
                'has_previous': False,
                'start_index': 0,
                'end_index': 0
            }
        }


def paginate_stored_procedure_results(data, request, page_size=20, max_page_size=1000):
    """
    Función de utilidad simple para paginar resultados de stored procedures.
    
    Args:
        data (list): Resultados completos del stored procedure
        request: Request de Django REST Framework
        page_size (int): Tamaño de página por defecto
        max_page_size (int): Tamaño máximo de página permitido
        
    Returns:
        dict: Respuesta paginada
        
    Ejemplo de uso:
        ```python
        # En tu vista
        all_results = [...]  # Resultados del stored procedure
        paginated_response = paginate_stored_procedure_results(
            all_results, request, page_size=25
        )
        return Response(paginated_response)
        ```
    """
    paginator = InMemoryPaginator(page_size=page_size, max_page_size=max_page_size)
    return paginator.paginate_data(data, request)


class StoredProcedureViewMixin:
    """
    Mixin para vistas que necesitan ejecutar stored procedures con paginación.
    """
    
    default_page_size = 20
    max_page_size = 1000
    
    def execute_and_paginate_stored_procedure(self, connection_name, procedure_name, 
                                            params, request):
        """
        Ejecuta un stored procedure y pagina los resultados.
        
        Args:
            connection_name (str): Nombre de la conexión (ej: 'extdb1')
            procedure_name (str): Nombre del stored procedure
            params (list): Parámetros para el stored procedure
            request: Request de Django REST Framework
            
        Returns:
            dict: Resultados paginados
        """
        from django.db import connections
        
        # Ejecutar stored procedure
        with connections[connection_name].cursor() as cursor:
            ref_cursor = cursor.connection.cursor()
            cursor.callproc(procedure_name, params + [ref_cursor])
            
            # Procesar resultados
            description = ref_cursor.description
            rows = ref_cursor.fetchall()
            results = [
                dict(zip([column[0] for column in description], row)) 
                for row in rows
            ]
        
        # Paginar resultados
        return paginate_stored_procedure_results(
            results, 
            request, 
            page_size=self.default_page_size,
            max_page_size=self.max_page_size
        )