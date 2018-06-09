// spam.cpp: DLL 응용 프로그램을 위해 내보낸 함수를 정의합니다.
//

#include "stdafx.h"

static PyObject* spam_SaveBookMark(PyObject* filename, PyObject* SID, PyObject* SName)
{
	std::string file;
	std::string name;
	std::string ID;

	if (!PyArg_ParseTuple(filename, "s", &file))
		return NULL;

	std::ofstream out(file);

	if (!PyArg_ParseTuple(SID, "s", &name))
		return NULL;

	if (!PyArg_ParseTuple(SName, "s", &ID))
		return NULL;

	out << name << " " << ID;
}

static PyMethodDef SpamMethods[] = {
	{ "SaveBookMark", (PyCFunction)spam_SaveBookMark, METH_VARARGS | METH_KEYWORDS, "save" },
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",
	"It is Test Module.",
	-1,
	SpamMethods
};
PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}
