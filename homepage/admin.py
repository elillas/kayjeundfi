from django.contrib import admin
from .models import HomepageSoftware, BlogAndReview, Message  # Import models to register in the admin interface
from .forms import HomepageSoftwareForm, BlogAndReviewForm  # Import custom forms for HomepageSoftware and BlogAndReview
from django.urls import reverse  # Import the reverse function to construct URLs based on view names and arguments
from django.http import HttpResponseRedirect  # Import HttpResponseRedirect to handle HTTP redirects

# Customizing the Django admin site headers and titles to change the site name and display in French
admin.site.site_header = "KayJeundFi Administration"
admin.site.site_title = "KayJeundFi Admin Portal"
admin.site.index_title = "Bienvenue sur KayJeundFi"


# Define a custom admin class for the HomepageSoftware model
class HomepageSoftwareAdmin(admin.ModelAdmin):
    form = HomepageSoftwareForm  # Specify the form to use in the admin interface


# Register the HomepageSoftware model with the custom admin class
admin.site.register(HomepageSoftware, HomepageSoftwareAdmin)


# Define a custom admin class for the BlogAndReview model
class BlogAndReviewAdmin(admin.ModelAdmin):
    form = BlogAndReviewForm  # Specify the form to use in the admin interface


# Register the BlogAndReview model with the custom admin class
admin.site.register(BlogAndReview, BlogAndReviewAdmin)


class MessageAdmin(admin.ModelAdmin):
    # Sets a custom template for the change form view in the admin interface
    change_form_template = 'admin/change_form.html'

    # Specify the fields to display in the list view of the Message model
    list_display = ('full_name', 'email', 'date_created',)

    # Make specific fields read-only based on whether the object is being edited
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            # Return a list of fields that should be read-only
            return self.readonly_fields + ('full_name', 'email', 'message', 'date_created')
        # Return the default readonly fields if no object is being edited
        return self.readonly_fields

    # Disallow the addition of new Message objects
    def has_add_permission(self, request):
        return False

    # Disallow changes to existing Message objects
    def has_change_permission(self, request, obj=None):
        return False

    # Override the response after deletion to redirect to the message section
    def response_delete(self, request, obj_display, obj_id):
        """
        Redirect to the message section after deletion.
        """
        # Perform the default delete action and get the response
        super().response_delete(request, obj_display, obj_id)
        # Redirect to the message section in the admin interface
        return HttpResponseRedirect(reverse('admin:homepage_message_changelist'))


# Register the Message model with the custom MessageAdmin class
admin.site.register(Message, MessageAdmin)
