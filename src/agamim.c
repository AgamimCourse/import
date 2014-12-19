#include <Python.h>

static PyMethodDef methods[] = {
    {NULL, NULL, 0, NULL, },
};

PyMODINIT_FUNC initagamim(void)
{
    Py_InitModule3("agamim", methods, "Agamim Values.");
}
