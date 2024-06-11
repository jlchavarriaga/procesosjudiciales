import unittest
from unittest.mock import patch, Mock
import requests_mock
from funciones_consulta import (
    obtener_numero_registros,
    obtener_registros,
    obtener_detalle_registro,
    obtener_actuaciones_judiciales
)
from main import obtener_registros_con_detalles_y_actuaciones


class TestFuncionesConsulta(unittest.TestCase):

    @requests_mock.Mocker()
    def test_obtener_numero_registros(self, mock_request):
        # Configurar el mock de la respuesta
        mock_response = {"total": 5}
        mock_request.post('https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/contarCausas', json=mock_response)

        resultado = obtener_numero_registros()
        self.assertEqual(resultado, mock_response)

    @requests_mock.Mocker()
    def test_obtener_registros(self, mock_request):
        # Configurar el mock de la respuesta
        mock_response = [{"idJuicio": "12345"}]
        mock_request.post('https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/buscarCausas?page=1&size=10', json=mock_response)

        resultado = obtener_registros(1, 10)
        self.assertEqual(resultado, mock_response)

    @requests_mock.Mocker()
    def test_obtener_detalle_registro(self, mock_request):
        # Configurar el mock de la respuesta
        mock_response = {"detalles": "Detalles de prueba"}
        mock_request.get('https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/getIncidenteJudicatura/12345', json=mock_response)

        resultado = obtener_detalle_registro('12345')
        self.assertEqual(resultado, mock_response)

    @requests_mock.Mocker()
    def test_obtener_actuaciones_judiciales(self, mock_request):
        # Configurar el mock de la respuesta
        mock_response = {"actuaciones": "Actuaciones de prueba"}
        payload = {
            "idMovimientoJuicioIncidente": 1,
            "idJuicio": "12345",
            "idJudicatura": "001",
            "idIncidenteJudicatura": 1,
            "aplicativo": "web",
            "nombreJudicatura": "JUZGADO DE PRUEBA",
            "incidente": 1
        }
        mock_request.post('https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/actuacionesJudiciales', json=mock_response)

        resultado = obtener_actuaciones_judiciales(1, "12345", "001", 1, "JUZGADO DE PRUEBA")
        self.assertEqual(resultado, mock_response)


class TestMain(unittest.TestCase):

    @patch('main.obtener_registros_con_detalles')
    @patch('main.obtener_actuaciones_judiciales')
    def test_obtener_registros_con_detalles_y_actuaciones(self, mock_obtener_actuaciones_judiciales, mock_obtener_registros_con_detalles):
        # Configurar los mocks de las funciones
        mock_detalle = {
            "idJuicio": "12345",
            "detalles": [
                {
                    "lstIncidenteJudicatura": [
                        {
                            "idMovimientoJuicioIncidente": 1,
                            "idIncidenteJudicatura": 1,
                            "idJudicaturaDestino": "001",
                            "nombreJudicatura": "JUZGADO DE PRUEBA"
                        }
                    ]
                }
            ]
        }
        mock_obtener_registros_con_detalles.return_value = [mock_detalle]
        mock_obtener_actuaciones_judiciales.return_value = {"actuaciones": "Actuaciones de prueba"}

        resultado = obtener_registros_con_detalles_y_actuaciones()
        self.assertEqual(resultado[0]['detalles'][0]['lstIncidenteJudicatura'][0]['actuacionesJudiciales'], {"actuaciones": "Actuaciones de prueba"})

if __name__ == '__main__':
    unittest.main()
