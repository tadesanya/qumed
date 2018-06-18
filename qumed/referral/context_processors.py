from qumed.constants import REFERRAL_STATUS


def include_constants(request):
    referral_status_dict = dict((x, x) for x, y in REFERRAL_STATUS)
    return referral_status_dict