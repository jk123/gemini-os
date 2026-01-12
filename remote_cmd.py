import os, platform, socket

# 1. Tiedoston luonti (mkdir & touch -simulaatio)
test_file = "gnode_chat_test.txt"
with open(test_file, "w") as f:
    f.write("Etähallinta testi suoritettu onnistuneesti chatista.\n")

# 2. Järjestelmätietojen haku
hostname = socket.gethostname()
os_info = platform.platform()
cpu_load = os.getloadavg()

print(f"--- GNODEN RAPORTTI ---")
print(f"Palvelin: {hostname}")
print(f"Käyttöjärjestelmä: {os_info}")
print(f"Kuormitus (1, 5, 15 min): {cpu_load}")
print(f"Tiedosto luotu: {os.path.abspath(test_file)}")
