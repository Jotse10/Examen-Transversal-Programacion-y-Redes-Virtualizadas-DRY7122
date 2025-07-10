while True:
    entrada = input("VLAN (numero o 's' para salir): ")
    if entrada.lower()=="s": break
    n = int(entrada)
    if 1 <= n <= 1005: tipo = "normal"
    elif 1006 <= n <= 4094: tipo = "extendido"
    else: tipo = "inválido"
    print(f"VLAN {n}: rango {tipo}")
