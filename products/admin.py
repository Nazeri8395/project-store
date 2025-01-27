from django.contrib import admin
from .models import Brand, FeatureValue, ProductFeature, ProductGroup, Product, Feature
from django.db.models.aggregates import Count
from django_admin_listfilter_dropdown.filters import DropdownFilter

class BrandAdmin(admin.ModelAdmin):
    list_display = ("brand_title",)
    list_filter = ("brand_title",)
    search_fields = ("brand_title",)
    ordering = ("brand_title",)
#==================================================================    
def de_active_product_group(modeladmin,request,queryset):
    res = queryset.update(is_active=False)
    if res == 1:
        message = "1 item was deactivated."
    else:
        message = f"{res} item was deactivated."
    modeladmin.message_user(request, message)

def active_product_group(modeladmin,request,queryset):
    res = queryset.update(is_active=True)
    if res == 1:
        message = "1 item was activated."
    else:
        message = f"{res} item was activated."
    modeladmin.message_user(request, message)

class ProductGroupInLineAdmin(admin.TabularInline):
    model = ProductGroup
    
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title', 'is_active', 'register_date', 'published_date', 'group_parent', 'count_sub_group')
    list_filter = ('group_title',('group_parent', DropdownFilter))
    search_fields = ('group_title',)
    ordering = ('group_title','group_parent')
    inlines = [ProductGroupInLineAdmin]
    actions = [de_active_product_group, active_product_group]
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin,self).get_queryset(args, **kwargs)
        qs = qs.annotate(sub_group=Count("groups"))
        return qs
    
    def count_sub_group(self,obj):
        return obj.sub_group
    
#====================================================================================
def de_active_product(modeladmin,request,queryset):
    res = queryset.update(is_active=False)
    if res == 1:
        message = "1 item was deactivated."
    else:
        message = f"{res} item was deactivated."
    modeladmin.message_user(request, message)

def active_product(modeladmin,request,queryset):
    res = queryset.update(is_active=True)
    if res == 1:
        message = "1 item was activated."
    else:
        message = f"{res} item was activated."
    modeladmin.message_user(request, message)

class ProductFeatureInLineAdmin(admin.TabularInline):
    model = ProductFeature
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','brand', 'price', 'published_date', 'display_product_group']
    list_filter = ("product_name",)
    search_fields = ("product_name",)
    ordering = ('product_name','published_date')
    actions = [de_active_product, active_product]
    inlines = [ProductFeatureInLineAdmin]
    
    def display_product_group(self,obj):
        queryset = Product.objects.prefetch_related('product_group')
        for obj in queryset:
            group_titles = [group.group_title for group in obj.product_group.all()]

        return group_titles
    
#==========================================================================
class FeatureValueInLine(admin.TabularInline):
    model = FeatureValue
    extra =3
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name', 'display_group', 'display_feature_values')
    list_filter = ('feature_name',)
    search_field = ('feature_name',)
    ordering = ('feature_name',)
    inlines = [FeatureValueInLine]
    
    def formfield_for_manytomany(self,db_field, request, **kwargs):
        if db_field.name == "Product_group":
            kwargs['queryset'] = ProductGroup.objects.filter(Q(group_parent=None))
            
        return super().formfield_for_manytomany(db_field, request,**kwargs)
    
    def display_group(self,obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])
    
    def display_feature_values(self,obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_values.all()])

admin.site.register(Brand,BrandAdmin)
admin.site.register(ProductGroup,ProductGroupAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Feature,FeatureAdmin)