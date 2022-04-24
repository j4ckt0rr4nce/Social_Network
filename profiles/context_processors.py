from .models import Profile, Relationship


def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.avatar

        return {'picture':pic}
    return {}


def inv_received_no(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = Relationship.objects.invitations_received(profile_obj).count

        return {'invites_no':qs_count}
    return {}
