from django.contrib.auth.models import Group,Permission


def create_group_permissions(sender, **kwargs):
        
        try:
#group creation
            readers_group, created = Group.objects.get_or_create(name='Readers')
            authors_group, created = Group.objects.get_or_create(name='Author')
            editors_group, created = Group.objects.get_or_create(name='Editor')

        #create permissions
            publish_permission, created = Permission.objects.get_or_create(codename="can_publish", content_type_id= "7", name="Can publish post")

            reader_permissions = [
            Permission.objects.get(codename="view_post")
            
        ]

            author_permissions  = [
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
            Permission.objects.get(codename="delete_post"),
             Permission.objects.get(codename="view_post"),

        ]

            editor_permissions = [
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
            Permission.objects.get(codename="delete_post"),
            publish_permission,
             Permission.objects.get(codename="view_post"),

        ]


        #setting permissions to the groups 

            readers_group.permissions.set(reader_permissions)
            authors_group.permissions.set(author_permissions)
            editors_group.permissions.set(editor_permissions)
            print("the group is created successfully")

        except Exception as e:
              print(f"the error is :{e}")