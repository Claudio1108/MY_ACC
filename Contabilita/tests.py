from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, Client
from django.conf import settings
from Contabilita import models as contabilita_models

from http import HTTPStatus
from django.urls import reverse
from Contabilita import views as contabilita_views

User = get_user_model()

def get_response(url_name, **kwargs):
    client = Client()
    if kwargs.get('authenticated_user', False):
        user = User.objects.create(username="foo", first_name="foo", last_name="boo")
        client.force_login(user)
    url = reverse(url_name)
    return client.get(url)


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
        self._test_template_view(AnonymousUser(), contabilita_views.viewHomePage, HTTPStatus.FOUND)

    def test_view_home_page_for_user(self):
        self._test_template_view(self.an_user, contabilita_views.viewHomePage, HTTPStatus.OK)

    def test_view_home_page_contabilita_for_anonymous_user(self):
        self._test_template_view(AnonymousUser(), contabilita_views.viewHomePageContabilita, HTTPStatus.FOUND)

    def test_view_home_page_contabilita_for_user(self):
        self._test_template_view(self.an_user, contabilita_views.viewHomePageContabilita, HTTPStatus.OK)

    def test_view_home_page_amministrazione_for_anonymous_user(self):
        self._test_template_view(AnonymousUser(), contabilita_views.viewHomePageAmministrazione, HTTPStatus.FOUND)

    def test_view_home_page_amministrazione_for_user(self):
        self._test_template_view(self.an_user, contabilita_views.viewHomePageAmministrazione, HTTPStatus.OK)

    def test_view_all_clients_for_anonymous_user(self):
        self._test_template_view(AnonymousUser(), contabilita_views.viewAllClienti.as_view(), HTTPStatus.FOUND)

    def test_view_all_clients_for_user(self):
        self._test_template_view(self.an_user, contabilita_views.viewAllClienti.as_view(), HTTPStatus.OK)

    def test_view_create_client_for_anonymous_user(self):
        self._test_template_view(AnonymousUser(), contabilita_views.viewCreateCliente.as_view(), HTTPStatus.FOUND)

    def test_view_create_client_for_user(self):
        self._test_template_view(self.an_user, contabilita_views.viewCreateCliente.as_view(), HTTPStatus.OK)


class GetAllClientiTest(TestCase):

    def test_get_all_clienti(self):
        contabilita_models.RubricaClienti.objects.create(
            nominativo='Mario Rossi', tel='3345678239', mail='mario.rossi@foo.it', note='Black')
        contabilita_models.RubricaClienti.objects.create(
            nominativo='Paolo Verdi', tel='3945528822', note='Green')
        contabilita_models.RubricaClienti.objects.create(
            nominativo='Carlo Gialli', tel='3567834222', mail='carlo.gialli@toto.it')
        contabilita_models.RubricaClienti.objects.create(
            nominativo='Gianni Neri', tel='3457612987')

        response = get_response("AllClienti", authenticated_user=True)
        values_in_context = response.context['filter_queryset']\
                               .order_by('nominativo').values()
        expected_values_in_context = contabilita_models.RubricaClienti.objects.all().order_by('nominativo').values()
        self.assertSequenceEqual(list(expected_values_in_context), list(values_in_context))

    def test_all_clienti_view_as_not_authenticated_user(self):
        response = get_response("AllClienti")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, f"{settings.LOGIN_URL}?next={reverse('AllClienti')}")

    def test_all_clienti_view_as_authenticated_user(self):
        response = get_response("AllClienti", authenticated_user=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "Amministrazione/Cliente/AllClienti.html")

class CreateClienteTest(TestCase):

    # def test_create_cliente(self):
    #     cliente = contabilita_models.RubricaClienti.objects.create(
    #                     nominativo='Mario Rossi', tel='3345678239', mail='mario.rossi@foo.it', note='Black')
    #     expected_create_client = contabilita_models.RubricaClienti.objects.get(id=cliente.id)
    #     self.assertEqual(cliente, expected_create_client)

    def test_create_cliente_view_as_not_authenticated_user(self):
        response = get_response("CreateCliente")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, f"{settings.LOGIN_URL}?next={reverse('CreateCliente')}")

    def test_create_cliente_view_as_authenticated_user(self):
        response = get_response("CreateCliente", authenticated_user=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "Amministrazione/Cliente/CreateCliente.html")


class ContabilitaViewClientTestCase(TestCase):
    def test_home_view_as_not_authenticated_user(self):
        """
        Il test e' esattamente come sopra, ma ovviamente fa una chiamata come se fosse
        un vero browser. In quest modo c'e' bisogno di usare le url
        """
        response = get_response("HomePage")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        """
        Se leggi la documentazione, settings.LOGIN_URL e' usato di default dal decorator
        login required e dovrebbe essere il modo per identificare l'url di login
        
        Nota: ci aspettiamo che la url restituita per il redirect contenga il next come 
        definito dalla documentazione di django.contrib.auth.
        """
        self.assertEqual(response.url, f"{settings.LOGIN_URL}?next={reverse('HomePage')}")

    def test_home_view_as_authenticated_user(self):
        """Test che va un poco piu' a fondo sul funzionamento della view

        Qui creiamo un vero login dell'user, perche' creiamo l'utente nel database. Non
        ci serve creare la password perche' siamo dio e nel backend facciamo cosa vogliam
        infatti forziamo il login.

        Forzando il login viene creata la sessione registrata all'utente.
        """
        response = get_response("HomePage", authenticated_user=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # ora che abbiamo il client, possiamo usare la response per testare
        # che il template corretto venga caricato
        self.assertTemplateUsed(response, "Homepage/HomePage.html")

    def test_home_contabilita_view_as_not_authenticated_user(self):
        response = get_response("HomePageContabilita")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, f"{settings.LOGIN_URL}?next={reverse('HomePageContabilita')}")

    def test_home_contabilita_view_as_authenticated_user(self):
        response = get_response("HomePageContabilita", authenticated_user=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "Homepage/HomePageContabilita.html")

    def test_home_amministrazione_view_as_not_authenticated_user(self):
        response = get_response("HomePageAmministrazione")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, f"{settings.LOGIN_URL}?next={reverse('HomePageAmministrazione')}")

    def test_home_amministrazione_view_as_authenticated_user(self):
        response = get_response("HomePageAmministrazione", authenticated_user=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "Homepage/HomePageAmministrazione.html")
