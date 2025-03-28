import os
from django.conf import settings
from django.db import connections
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from ..core.models import SQLQuery
from .models import ExtOrderMaster, ExtOrderItem
from .serializers import ExtOrderMasterSerializer, ExtOrderMasterOnlySerializer, ExtOrderItemSerializer


class CategoryBrandListAPIView(APIView):
    """ This view returns the list of Departments (DEPTO), Categories (CAT), or Subcategories (SUBCAT)
        along with the brands associated with each of them.
        Parameters: p01, p02
        p01 - Type of list (DEPTO, CAT, SUBCAT)
        p02 - Company
        The list returned depends on the value of the parameter passed to the query (p01).
        For example, if p01 = 'DEPTO', the list of departments with the brands associated with each of them will be returned.
        If p01 = 'CAT', the list of categories with the brands associated with each of them will be returned.
        If p01 = 'SUBCAT', the list of subcategories with the brands associated with each of them will be returned.
        If p01 = 'X', an error message will be returned.
    """
    # Vista 35
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        idVista = 35
        # p01 - List type (DEPTO, CAT, SUBCAT)
        # p02 - Company

        p01 = str(request.query_params.get('p01', 'X'))
        p02 = str(request.query_params.get('p02', '01'))

        if p01 == 'X':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p02]

        qrys = SQLQuery.objects.filter(vista=idVista)

        result = []
        # qrycalling = 'DMC.LINAEE_CATSBRANDS'
        qrycalling = qrys[0].content
        
        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class ProductsAPIView(APIView):
    """ Returns the list of products according to the filters passed as parameters.
        Parameters: depto, cat, scat, brands, cia
        depto - Department
        cat - Category
        scat - Subcategory
        brands - Brands
        cia - Company
        If no parameters are passed, an error message will be returned.
    """
    # Vista 36
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        idVista = 36
        # depto - DEPARTMENT filter
        # cat - CATEGORY filter
        # scat - SUBCATEGORY filter
        # brands - BRAND filter EJ.: '200,101,151,25'
        # cia - COMPANY filter

        p01 = str(request.query_params.get('depto', '0')).lower().strip()
        p02 = str(request.query_params.get('cat', '0')).lower().strip()
        p03 = str(request.query_params.get('scat', '0')).lower().strip()
        p04_raw = str(request.query_params.get('brands', '')).strip()
        p05 = str(request.query_params.get('cia', '01')).lower().strip()

        # Transform p04 to be compatible with the procedure
        if p04_raw:
            p04_list = p04_raw.split(",")  # Split by commas
            # Add single quotes to each element and join them with commas. EJ.: '200','101','151','25'
            p04 = ",".join([f"'{brand.strip()}'" for brand in p04_list])
        else:
            p04 = ""  # If there are no brands, leave the parameter empty

        pvals = p01 + p02 + p03 + p04 + p05

        if pvals == '00001':
            return Response([{"RESULT": "NO DATA"}], status=status.HTTP_200_OK)

        params = [p01, p02, p03, p04, p05]

        qrys = SQLQuery.objects.filter(vista=idVista)

        result = []
        # qrycalling = 'DMC.LINAEE_SHOPPINGCARTPRODUCTS'
        qrycalling = qrys[0].content

        with connections['extdb1'].cursor() as cursor:

            refCursor = cursor.connection.cursor()

            cursor.callproc(qrycalling, params + [refCursor])

            descrip = refCursor.description

            rows = refCursor.fetchall()

            result = [dict(zip([column[0] for column in descrip], row)) for row in rows]

        return Response(result, status=status.HTTP_200_OK)


class ItemImagesAPIView(APIView):
    """
    View to list all images in a given subfolder.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, subfolder, format=None):
        # Define the path to the images folder
        images_path = os.path.join(settings.MEDIA_ROOT, 'fotos', subfolder)

        if not os.path.exists(images_path):
            return Response({"error": "Subfolder does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # List all files in the subfolder
        images = [f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))]

        # Create URLs for the images
        image_urls = [request.build_absolute_uri(os.path.join(settings.MEDIA_URL, 'fotos', subfolder, image)) for image in images]

        return Response(image_urls, status=status.HTTP_200_OK)


class ExtOrderMasterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing ExtOrderMaster.
    Including the items associated with each order.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = ExtOrderMaster.objects.all()
    serializer_class = ExtOrderMasterSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'created_ad', 'status', 'created_by__username', 'customer_name']
    ordering_fields = ['id', 'created_at', 'status', 'created_by__username', 'customer_name']

    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class ExtOrderMasterOnlyViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing ExtOrderMaster.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = ExtOrderMaster.objects.all()
    serializer_class = ExtOrderMasterOnlySerializer


class ExtOrderItemViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing ExtOrderItem.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = ExtOrderItem.objects.all()
    serializer_class = ExtOrderItemSerializer


