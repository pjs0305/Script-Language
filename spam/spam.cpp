//spam.cpp: DLL 응용 프로그램을 위해 내보낸 함수를 정의합니다.

#include"stdafx.h"

static PyObject* MakeURL1(PyObject *self, PyObject *psearch)
{
	std::string baseURL = "http://openapi.tago.go.kr/openapi/service/SubwayInfoService/";
	std::string key = "serviceKey=QCt6OJN%2BX%2BK%2F1QWhl3xAV6wrYByNl7oLDFyYobuvd%2FXsKryONWzAm0FH9zbTDU0syJHEkFxCHE31CKqoCcUIKg%3D%3D";

	char* csearch;
	if (!PyArg_ParseTuple(psearch, "s", &csearch))
		return NULL;
	std::string search(csearch);

	baseURL += search;
	baseURL += "?";
	baseURL += key;
	baseURL += "&";

	return Py_BuildValue("s", baseURL.c_str());
}


static PyObject* MakeURL2(PyObject *self, PyObject* args, PyObject* Keywords)
{
	static const char* Station[] = { "subwayStationName", NULL }; // 지하철역 검색
	static const char* BB[] = { "subwayStationId", NULL }; // 건물, 버스 검색
	static const char* Schedule[] = { "subwayStationId", "dailyTypeCode", "upDownTypeCode", NULL }; // 시간표 검색


	PyObject* KeyList = PyDict_Keys(Keywords); // 사전의 키값 뽑아오기(리스트로)
	int n = PyDict_Size(Keywords); // 뽑아온 리스트의 크기


	char* cname = NULL;
	char* cid = NULL;
	char* cdtcode = NULL;
	char* cudtcode = NULL;

	std::string keynames;
	switch (n)
	{
	case 1:
		char* keyname; // 키 하나 뽑기

		PyArg_Parse(PyList_GetItem(KeyList, 0), "s", &keyname); // 키 하나 뽑아옴
		keynames = keyname;

		if (keynames == "subwayStationName")
		{
			PyArg_ParseTupleAndKeywords(args, Keywords, "s", (char**)Station, &cname);
		}
		else
		{
			PyArg_ParseTupleAndKeywords(args, Keywords, "s", (char**)BB, &cid);
		}
		break;
	case 3:
		PyArg_ParseTupleAndKeywords(args, Keywords, "sss", (char**)Schedule, &cid, &cdtcode, &cudtcode);
		break;
	default:
		return NULL;
	}

	std::string baseURL;

	std::string name;
	if (cname)
		name = cname;
		
	std::string id;
	if (cid)
		id = cid;

	std::string dtcode;
	if (cdtcode)
		dtcode = cdtcode;

	std::string udtcode;
	if (cudtcode)
		udtcode = cudtcode;

	if (name.length())
	{
		baseURL += "subwayStationName=" + name + "&";
	}
	if (id.length())
	{
		baseURL += "subwayStationId=" + id + "&";
	}
	if (dtcode.length())
	{
		baseURL += "dailyTypeCode=" + dtcode + "&";
	}
	if (udtcode.length())
	{
		baseURL += "upDownTypeCode=" + udtcode + "&";
	}

	baseURL += "numOfRows=1000";

	return Py_BuildValue("s", baseURL.c_str());
}

static PyMethodDef Method[] = {
	{ "MakeURL1", (PyCFunction)MakeURL1, METH_VARARGS, "Make URL Step 1" },
	{ "MakeURL2", (PyCFunction)MakeURL2, METH_VARARGS | METH_KEYWORDS, "Make URL Step 2" },
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
	PyModuleDef_HEAD_INIT,
	"func",
	"Test",
	-1,
	Method
};

PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&Module);
}
