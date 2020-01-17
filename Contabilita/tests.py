from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

from http import HTTPStatus

from Contabilita.views import viewHomePage

User = get_user_model()


class ContabilitaViewsTestCase(TestCase):
    """
    Al momento questa semplice classe fa due test distinti su una function view la prima cosa che
    puoi notare e' che il codice e' molto simile, inoltre non c'e' un controllo che il template
    renderizzato e' quello giusto e che il context passato e' quello che ti aspetti.

    Per fare questo tipo di controllo e' necessario usare il client che a volte e' un po' troppo
    lento perche' si carica tutta l'app, ma volendo si puo' usare come strategia
    """
    def setUp(self) -> None:
        self.factory = RequestFactory()  # e' una request "finta"
        self.an_user = User.objects.create(email="foo@boo.com")

    def test_view_home_page_for_anonymous_user(self):
        request = self.factory.get(path="/foo/boo")
        request.user = AnonymousUser()  # simula l'utente non loggato
        response = viewHomePage(request)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302

    def test_view_home_page_for_user(self):
        request = self.factory.get(path="/foo/boo")
        request.user = self.an_user  # simula l'utente loggato
        response = viewHomePage(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200


