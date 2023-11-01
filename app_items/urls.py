from django.urls import path
from . import views
urlpatterns = [
    path('choice', views.choice, name='choice'),
    path('log', views.log, name='log'),
    path('item', views.item, name='item'),
    path('presale', views.presale, name='presale'),
    path('search', views.search, name='search'),
    path('card/<int:item_id>', views.card, name='card'),
    path('update/<int:item_id>', views.update, name='update'),
    path('pending', views.pending, name='pending'),
    path('expiring', views.expiring, name='expiring'),
    path('shop_hold', views.shop_hold, name='shop_hold'),
    path('commercial', views.commercial, name='commercial'),
    

    # path('GeneratePDF/<pk>', views.GeneratePDF.as_view(), name="GeneratePDF"),
    path('DownloadPDF', views.DownloadPDF.as_view(), name="DownloadPDF"),
    path('DownloadPDF_log', views.DownloadPDF_log.as_view(), name="DownloadPDF_log"),
    path('DownloadPDF_presale', views.DownloadPDF_presale.as_view(), name="DownloadPDF_presale"),
]
