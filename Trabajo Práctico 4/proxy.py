import subprocess

class Ping:
    def __init__(self, attempts: int = 10):
        self.attempts = attempts

    def execute(self, ip: str):
        """Sólo hace ping si la IP comienza con '192.'"""
        if not ip.startswith("192."):
            raise ValueError(f"Dirección no permitida: {ip}")
        return self._do_ping(ip)

    def executefree(self, ip: str):
        """Hace ping sin restricción de IP."""
        return self._do_ping(ip)

    def _do_ping(self, ip: str):
        cmd = ["ping", "-c", str(self.attempts), ip]
        print(f"Haciendo ping a {ip} ({self.attempts} intentos)…")
        return subprocess.run(cmd, capture_output=True, text=True).stdout

class PingProxy:
    def __init__(self):
        self._ping = Ping()

    def execute(self, ip: str):
        """Si la IP es 192.168.0.254, redirige a www.google.com vía ejecutefree; si no, delega a execute."""
        if ip == "192.168.0.254":
            print("Proxy interceptó IP crítica; usando google.com sin restricción.")
            return self._ping.executefree("www.google.com")
        else:
            print("Proxy delega ping normal.")
            return self._ping.execute(ip)

# Ejemplo de uso:
if __name__ == "__main__":
    proxy = PingProxy()
    try:
        salida1 = proxy.execute("192.168.0.254")
        print(salida1)
        salida2 = proxy.execute("192.168.1.10")
        print(salida2)
        # Este último lanzará excepción en Ping.execute
        proxy.execute("10.0.0.5")
    except ValueError as e:
        print(f"Error: {e}")
