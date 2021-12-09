from django.test import SimpleTestCase
from django.urls import reverse,resolve
from app import views
from django.contrib.auth import views as auth_views
class TestUrls(SimpleTestCase):
    def test_home(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func.__name__,views.ProductView.__name__)
    
    def test_product_detail(self):
        url = reverse("product-detail",args=[1])
        self.assertEquals(resolve(url).func.__name__,views.ProductDetailView.__name__)
    def test_search_product(self):
        url = reverse("searchproduct")
        self.assertEquals(resolve(url).func.__name__,views.searchproduct.__name__)
    def test_search_product_image(self):
        url = reverse("searchproductimage")
        self.assertEquals(resolve(url).func.__name__,views.searchproductimage.__name__)
    def test_add_to_cart(self):
        url = reverse("add-to-cart")
        self.assertEquals(resolve(url).func.__name__,views.add_to_cart.__name__)
    def test_wishlist(self):
        url = reverse("wishlist")
        self.assertEquals(resolve(url).func.__name__,views.show_wishlist.__name__)
    def test_add_to_wishlist(self):
        url = reverse("add_to_wishlist")
        self.assertEquals(resolve(url).func.__name__,views.add_to_wishlist.__name__)
    def test_delete_review(self):
        url = reverse("deletewishlist")
        self.assertEquals(resolve(url).func.__name__,views.deletewishlist.__name__)
    def test_delete_review(self):
        url = reverse("deletereview")
        self.assertEquals(resolve(url).func.__name__,views.deletereview.__name__)
    def test_plus_cart(self):
        url = reverse("pluscart")
        self.assertEquals(resolve(url).func.__name__,views.plus_cart.__name__)
    def test_minus_cart(self):
        url = reverse("minuscart")
        self.assertEquals(resolve(url).func.__name__,views.minus_cart.__name__)
    def test_remove_cart(self):
        url = reverse("removecart")
        self.assertEquals(resolve(url).func.__name__,views.remove_cart.__name__)
    def test_buy_now(self):
        url = reverse("buynow")
        self.assertEquals(resolve(url).func.__name__,views.buynow.__name__)
    def test_add_review(self):
        url = reverse("addreview")
        self.assertEquals(resolve(url).func.__name__,views.ReviewView.__name__)
    def test_profile(self):
        url = reverse("profile")
        self.assertEquals(resolve(url).func.__name__,views.ProfileView.__name__)
    def testaddress(self):
        url = reverse("address")
        self.assertEquals(resolve(url).func.__name__,views.address.__name__)
    def test_delete_address(self):
        url = reverse("deleteaddress")
        self.assertEquals(resolve(url).func.__name__,views.deleteaddress.__name__)
    def test_orders(self):
        url = reverse("orders")
        self.assertEquals(resolve(url).func.__name__,views.orders.__name__)
    def test_change_password(self):
        url = reverse("changepassword")
        self.assertEquals(resolve(url).func.__name__,auth_views.PasswordChangeView.__name__)
    def test_passwordchangedone(self):
        url = reverse("passwordchangedone")
        self.assertEquals(resolve(url).func.__name__,auth_views.PasswordChangeView.__name__)
    def test_accoustic_guitar(self):
        url = reverse("acousticguitar")
        self.assertEquals(resolve(url).func.__name__,views.acousticguitar.__name__)
    def test_login(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func.__name__,auth_views.LoginView.__name__)
    def test_reset(self):
        url = reverse("password_reset")
        self.assertEquals(resolve(url).func.__name__,auth_views.PasswordResetView.__name__)
    def test_admin_dashboard(self):
        url = reverse("admin-dashboard")
        self.assertEqual(resolve(url).func.__name__,views.dashboard.__name__)
    def test_admin_add_product(self):
        url = reverse("add-product")
        self.assertEqual(resolve(url).func.__name__,views.addProduct.__name__)
    def test_admin_create_product(self):
        url = reverse("create-product")
        self.assertEquals(resolve(url).func.__name__,views.createProduct.__name__)
    def test_admin_update_product(self):
        url = reverse("update-product",args = ["test"])
        self.assertEquals(resolve(url).func.__name__,views.updateProduct.__name__)
    def test_admin_sales(self):
        url = reverse("sales-forecasting")
        self.assertEquals(resolve(url).func.__name__,views.salesForecasting.__name__)
