from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, Client
from django.conf import settings

from http import HTTPStatus

from django.urls import reverse

# from Contabilita.views import viewHomePage

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


class ContabilitaViewClientTestCase(TestCase):

    def test_home_view_as_not_authenticated_user(self):
        """
        Il test e' esattamente come sopra, ma ovviamente fa una chiamata come se fosse
        un vero browser. In quest modo c'e' bisogno di usare le url
        """
        client = Client()
        url = reverse("HomePage")
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        """
        Se leggi la documentazione, settings.LOGIN_URL e' usato di default dal decorator
        login required e dovrebbe essere il modo per identificare l'url di login
        """
        self.assertEqual(response.url, settings.LOGIN_URL)

    def test_home_view_as_authenticated_user(self):
        """Test che va un poco piu' a fondo sul funzionamento della view

        Qui creiamo un vero login dell'user, perche' creiamo l'utente nel database. Non
        ci serve creare la password perche' siamo dio e nel backend facciamo cosa vogliam
        infatti forziamo il login.

        Forzando il login viene creata la sessione registrata all'utente.
        """
        user = User.objects.create(username="foo", first_name="foo", last_name="boo")
        client = Client()
        client.force_login(user)
        url = reverse("HomePage")
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # ora che abbiamo il client, possiamo usare la response per testare
        # che il template corretto venga caricato
        self.assertTemplateUsed(response, "Homepage/HomePage.html")

