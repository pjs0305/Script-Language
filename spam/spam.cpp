// spam.cpp: DLL 응용 프로그램을 위해 내보낸 함수를 정의합니다.
//

#include "stdafx.h"

void spam_SaveBookMark(PyObject *self, PyObject* arg, PyObject* karg)
{
	std::string name;
	std::string ID;

	return;
}

//static PyObject* spam_SaveBookMark(PyObject *self, PyObject* filename, PyObject* valarg, PyObject* karg)
//{
//	std::string file;
//	std::string name;
//	std::string ID;
//	char* kwlist[] = { const_cast<char*>("ID"), const_cast<char*>("name"), NULL };
//
//	if (!PyArg_ParseTuple(filename, "s", &file))
//		return NULL;
//
//	std::ofstream out(file);
//
//	if (!PyArg_ParseTupleAndKeywords(valarg, karg, "s|s", kwlist, ID, name))
//		return NULL;
//
//	out << name << " " << ID;
//}

static PyMethodDef SaveMethod[] = {
	{ "SaveBookMark", (PyCFunction)spam_SaveBookMark, METH_VARARGS, "save" },
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef SaveModule = {
	PyModuleDef_HEAD_INIT,
	"spam",
	"It is Test Module.",
	-1,
	SaveMethod
};

PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&SaveModule);
}
