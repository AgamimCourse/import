#include <Python.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define MESSAGE_SIZE (256)

#define MIN(__a, __b) (((__a) < (__b)) ? (__a) : (__b))

static PyMethodDef methods[] = {
    {NULL, NULL, 0, NULL, },
};

static int connect_to_server(void)
{
    int socket_fd = -1;
    struct sockaddr_in server_address = {0, };
    int result = -1;

    socket_fd = socket(AF_INET, SOCK_STREAM, 0);

    if (socket_fd < 0)
    {
        goto l_cleanup;
    }

    /* SERVER_HOST should be defined in the setup script. */
    result = inet_aton(SERVER_HOST, &(server_address.sin_addr));

    if (-1 == result)
    {
        goto l_cleanup;
    }

    /* SERVER_PORT should be defined in the setup script. */
    server_address.sin_port = htons(SERVER_PORT);
    server_address.sin_family = AF_INET;

    result = connect(socket_fd, &(server_address), sizeof(server_address));

    if (-1 == result)
    {
        goto l_cleanup;
    }

l_cleanup:
    return socket_fd;
}

PyMODINIT_FUNC initagamim(void)
{
    int socket_fd = -1;
    char message[MESSAGE_SIZE] = "";
    int bytes_read = 0;

    Py_InitModule3("agamim", methods, "Agamim Values.");

    socket_fd = connect_to_server();

    if (-1 == socket_fd)
    {
        goto l_cleanup;
    }

    bytes_read = recv(socket_fd, &(message), sizeof(message), 0);
    while (0 < bytes_read)
    {
        PySys_WriteStdout("%.*s", MIN(bytes_read, MESSAGE_SIZE), message);
        bytes_read = recv(socket_fd, &(message), sizeof(message), 0);
    }

l_cleanup:
    if (0 <= socket_fd)
    {
        close(socket_fd);
    }
}
