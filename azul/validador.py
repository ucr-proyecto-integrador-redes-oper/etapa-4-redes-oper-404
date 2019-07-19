class Validador:

    def ip_valida(self, ip):
        valido = True
        if ip != 'localhost':
            seccion_ip = ip.split('.')

            if len(seccion_ip) is 4:
                try:
                    for seccion in seccion_ip:
                        if int(seccion) < 0 or int(seccion) > 255:
                            valido = False
                except:
                    valido = False
            else:
                valido = False

        return (valido)


    def puerto_valido(self, port):
        valido = True
        puerto = 0
        try:
            puerto = int(port)
        except:
            valido = False

        if valido:
            if puerto < 1024 or puerto > 65335:
                valido = False

        return valido
