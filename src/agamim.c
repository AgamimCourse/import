#include <Python.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define MESSAGE_SIZE (256)

static PyMethodDef methods[] = {
    {NULL, NULL, 0, NULL, },
};

PyMODINIT_FUNC initagamim(void)
{
    int socket_fd = -1;
    struct sockaddr_in server_address = {0, };
    char message[MESSAGE_SIZE] = "";
    int bytes_read = 0;
    int result = -1;

    Py_InitModule3("agamim", methods, "Agamim Values.");

    socket_fd = socket(AF_INET, SOCK_STREAM, 0);

    if (socket_fd < 0)
    {
        goto l_cleanup;
    }

    result = inet_aton(SERVER_HOST, &(server_address.sin_addr));

    if (-1 == result)
    {
        goto l_cleanup;
    }

    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(SERVER_PORT);

    result = connect(socket_fd, &(server_address), sizeof(server_address));

    if (-1 == result)
    {
        goto l_cleanup;
    }

    bytes_read = recv(socket_fd, &(message), MESSAGE_SIZE, 0);
    while (0 < bytes_read)
    {
        PySys_WriteStdout("%s", message);
        bytes_read = recv(socket_fd, &(message), MESSAGE_SIZE, 0);
    }

l_cleanup:
    if (0 <= socket_fd)
    {
        close(socket_fd);
    }
}
