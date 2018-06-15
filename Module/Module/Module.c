#include<Python.h>
#include<stdio.h>

void Func(PyObject *self, PyObject* args, PyObject* Keywords)
{
	int a;
	int b;
	static char* keywordlist[] = { "a", "b", NULL };

	PyArg_ParseTupleAndKeywords(args, Keywords, "i|i", keywordlist, &a, &b);

	printf("%d %d", a, b);
}

static PyMethodDef Method[] = {
	{ "Test", (PyCFunction)Func, METH_VARARGS | METH_KEYWORDS, "Test Func" },
{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef Module = {
	PyModuleDef_HEAD_INIT,
	"Module",
	"Test Func",
	-1,
	Method
};

PyMODINIT_FUNC
PyInit_Module(void)
{
	return PyModule_Create(&Module);
}
