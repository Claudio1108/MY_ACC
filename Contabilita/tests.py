from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, Client
from django.conf import settings
from .models import *

from http import HTTPStatus
from django.urls import reverse
from Contabilita.views import viewHomePage, viewHomePageAmministrazione, viewHomePageContabilita, viewAllClienti, viewCreateCliente

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

    def _test_template_view(self, usr, view, expected_status):
        request = self.factory.get(path="/foo/boo")
        request.user = usr
        response = view(request)
        self.assertEqual(response.status_code, expected_status)

    def test_view_home_page_for_anonymous_user(self):
        self._test_template_view(AnonymousUser(), viewHomePage, HTTPStatus.FOUND)

    def test_view_home_page_for_user(self):
        self._test_template_view(self.an_user, viewHomePage, HTTPStatus.OK)

    def test_view_home_page_contabilita_for_anonymous_user(self):
        self._test_template_view(AnonymousUser(), viewHomePageContabilita, HTTPStatus.FOUND)

    def test_view_home_page_contabilita_for_user(self):
        self._test_template_view(self.an_user, viewHomePageContabilita, HTTPStatus.OK)

    def test_view_home_page_amministrazione_for_anonymous_user(self):
        self._test_template_view(AnonymousUser(), viewHomePageAmministrazione, HTTPStatus.FOUND)

    def test_view_home_page_amministrazione_for_user(self):
        self._test_template_view(self.an_user, viewHomePageAmministrazione, HTTPStatus.OK)

    def test_view_all_clients_for_anonymous_user(self):
        self._test_template_view(AnonymousUser(), viewAllClienti.as_view(), HTTPStatus.FOUND)

    def test_view_all_clients_for_user(self):
        self._test_template_view(self.an_user, viewAllClienti.as_view(), HTTPStatus.OK)

    def test_view_create_client_for_anonymous_user(self):
        self._test_template_view(AnonymousUser(), viewCreateCliente.as_view(), HTTPStatus.FOUND)

    def test_view_create_client_for_user(self):
        self._test_template_view(self.an_user, viewCreateCliente.as_view(), HTTPStatus.OK)


class GetAllClientiTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="foo", first_name="foo", last_name="boo")
        RubricaClienti.objects.create(
            nominativo='Mario Rossi', tel='3345678239', mail='mario.rossi@foo.it', note='Black')
        RubricaClienti.objects.create(
            nominativo='Paolo Verdi', tel='3945528822', note='Green')
        RubricaClienti.objects.create(
            nominativo='Carlo Gialli', tel='3567834222', mail='carlo.gialli@toto.it')
        RubricaClienti.objects.create(
            nominativo='Gianni Neri', tel='3457612987')

    def test_get_all_clienti(self):
        self.client.force_login(self.user)
        rendering_values = self.client.get('/AllClienti/').context['filter_queryset'].order_by('nominativo').values() # valori effettivamente renderizzati
        db_values = RubricaClienti.objects.all().order_by('nominativo').values() # valori presenti nel db di testing
        self.assertListEqual(list(db_values), list(rendering_values))

    def test_template_render(self):
        self.client.force_login(self.user)
        url = reverse('AllClienti')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Amministrazione/Cliente/AllClienti.html')


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
        
        Nota: ci aspettiamo che la url restituita per il redirect contenga il next come 
        definito dalla documentazione di django.contrib.auth.
        """
        self.assertEqual(response.url, f"{settings.LOGIN_URL}?next={url}")

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
