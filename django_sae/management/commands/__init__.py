# coding=utf-8


def patch_for_sae_restful_mysql():
    from sae._restful_mysql import monkey

    monkey.patch()