//spam.cpp: DLL 응용 프로그램을 위해 내보낸 함수를 정의합니다.

#include"stdafx.h"

//static PyObject* GetSubWayLine(PyObject *self, PyObject *pID)
//{
//	char* ID;
//
//	if (!PyArg_ParseTuple(pID, "s", &ID))
//		return NULL;
//
//	std::string sID(ID);
//
//	std::string LineId{ sID.begin() + 3, sID.end() };
//
//	std::string Line;
//
//	if (LineId.length() == 3)
//	{
//		if (LineId[0] == '1')
//		{
//			if (LineId[1] != '9')
//			{
//				Line = LineId[0] + "호선";
//			}
//			else
//			{
//				if (LineId[2] == '0')
//				{
//					Line = LineId[0] +std::string{"호선"};
//				}
//				else
//				{
//					Line =std::string{"경의중앙선"};
//				}
//			}
//		}
//		else
//		{
//			Line = LineId[0] +std::string{ "호선"};
//		}
//	}
//	else if (LineId.length() == 4)
//	{
//		if (LineId[0] == '1')
//		{
//			if (LineId[1] == '1')
//			{
//				Line =std::string{ "1호선"};
//			}
//			else if ('2' <= LineId[1] <= '3')
//			{
//				Line =std::string{ "경의중앙선"};
//			}
//			else if (LineId[1] == '4')
//			{
//				Line =std::string{ "1호선"};
//			}
//			else if (LineId[1] == '5')
//			{
//				Line =std::string{ "분당선"};
//			}
//			else if (LineId[1] == '6')
//			{
//				Line =std::string{ "경의중앙선"};
//			}
//			else if (LineId[1] == '7')
//			{
//				Line =std::string{ "에버라인"};
//			}
//			else if (LineId[1] == '8')
//			{
//				Line =std::string{ "경춘선"};
//			}
//			else if (LineId[1] == '9')
//			{
//				Line =std::string{ "신분당선"};
//			}
//		}
//		else if (LineId[0] == '4')
//		{
//			if (LineId[1] == '0')
//			{
//
//				Line =std::string{ "공항철도"};
//			}
//			else if (LineId[1] == '1')
//			{
//				Line =std::string{ "자기부상철도"};
//			}
//		}
//	}
//	else if (LineId.length() == 5)
//	{
//		if (LineId[0] == '1')
//		{
//			if (LineId[2] == '0')
//			{
//				Line =std::string{ "의정부경전철"};
//			}
//			else if (LineId[2] == '1')
//			{
//				Line =std::string{ "수인선"};
//			}
//			else if (LineId[2] == '2')
//			{
//				Line =std::string{ "경강선"};
//			}
//			else if (LineId[2] == '3')
//			{
//				Line =std::string{ "우이신설선"};
//			}
//		}
//		else if (LineId[0] == '2')
//		{
//			if (LineId[2] == '1')
//			{
//				Line =std::string{ "인천1호선"};
//			}
//			else if (LineId[2] == '2')
//			{
//				Line =std::string{ "인천2호선"};
//			}
//		}
//		else if (LineId[0] == '3')
//		{
//			Line =std::string{ "대전1호선"};
//		}
//		else if (LineId[0] == '4')
//		{
//			if (LineId[2] == '1')
//			{
//				Line =std::string{ "대구1호선"};
//			}
//			else if (LineId[2] == '2')
//			{
//				Line =std::string{ "대구2호선"};
//			}
//			else if (LineId[2] == '3')
//			{
//				Line =std::string{ "대구3호선"};
//			}
//		}
//		else if (LineId[0] == '5')
//		{
//			Line =std::string{ "광주1호선"};
//		}
//		else if (LineId[0] == '7')
//		{
//			if ('0' <= LineId[2] < '2')
//			{
//				Line =std::string{ "부산1호선"};
//			}
//			else if (LineId[2] == '2')
//			{
//				Line =std::string{ "부산2호선"};
//			}
//			else if (LineId[2] == '3')
//			{
//				Line =std::string{ "부산3호선"};
//			}
//			else if (LineId[2] == '4')
//			{
//				Line =std::string{ "부산4호선"};
//			}
//			else if (LineId[2] == '8')
//			{
//				Line =std::string{ "부산동해선"};
//			}
//			else if (LineId[2] == '9')
//			{
//				Line =std::string{ "부산김해경전철"};
//			}
//		}
//	}
//
//	PyUnicode_FromString(Line.c_str());
//	return Py_BuildValue("O", PyUnicode_FromString(Line.c_str()));
//}
//
//static PyMethodDef GetMethod[] = {
//	{ "GetSubWayLine", GetSubWayLine, METH_VARARGS, "Check subway line through Subway station." },
//	{ NULL, NULL, 0, NULL }
//};
//
//static struct PyModuleDef GetModule = {
//	PyModuleDef_HEAD_INIT,
//	"spam",
//	"Subway Line.",
//	-1,
//	GetMethod
//};
//
//PyMODINIT_FUNC
//PyInit_spam(void)
//{
//	return PyModule_Create(&GetModule);
//}
// spam.cpp: DLL 응용 프로그램을 위해 내보낸 함수를 정의합니다.
//

static PyObject* Func(PyObject *self, PyObject* url, PyObject* search, PyObject* Key, PyObject* )
{
	auto pName = PyUnicode_FromString("한글");

	auto pModule = PyImport_Import(pName); 
	Py_DECREF(pName);
	
	return pName;


}

static PyMethodDef Method[] = {
	{ "Test", (PyCFunction)Func, METH_VARARGS, "Test" },
{ NULL, NULL, 0, NULL }
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
