import math
import struct
import matplotlib.pyplot as plt

#ovo je funkcija koja nalazi distance, odnosno udaljenost izmedju dve tacke
# zadate geografskom duzinom i sirinom
def haversine(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = math.sqrt(
        (math.sin(delta_lat / 2)) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(delta_lon / 2)) ** 2)
    d = 2 * 6371000 * math.asin(a)
    return d

# funkcija koja na osnovu koordinati pronalazi odgovarajuci hgt file i cita nadmorsku visinu tackeS
def get_elevation(n, e):
    imefjla = "N" + str(math.trunc(n)) + "E0" + str(math.trunc(e)) + ".hgt"
    i = n - math.trunc(n)
    j = e - math.trunc(e)
    vrsta = round(i * 1200)
    kolona = round(j * 1200)
    pozicija = (1201 * (1201 - vrsta - 1) + kolona) * 2
    f=open(imefjla, "rb")
    f.seek(pozicija)
    buf = f.read(2)
    val = struct.unpack('>h', buf)
    if not val == -32768:
       return val
    else:
       return None


if __name__ == "__main__":
    #koordinate prve tacke

    nort1 = float(input("Unesite severnu geografsku sirinu prve tacke: "))

    east1 = float(input("Unesite istocnu geografsku duzinu prve tacke: "))
    # koordinate druge tacke
    nort2 = float(input("Unesite severnu geografsku sirinu prve tacke: "))

    east2 = float(input("Unesite istocnu geografsku duzinu druge tacke: "))


    #koordinate koje smo mi koristili za demonstraciju :
    #43.4111904, 20.35528255 - Golija
    #43.3211424, 21.89567149  - Nis

    P1 = [nort1, east1]
    P2 = [nort2, east2]

    # najkraca udaljenost izmedju P1 i P2
    distanca = haversine(nort1, east1, nort2, east2)

    s = 100

    interval_lat = (P2[0] - P1[0]) / s  # interval za dobijanje latitude tacaka izmedju P2 i P1
    interval_lon = (P2[1] - P1[1]) / s  # interval za longitude


    lat0 = P1[0]
    lon0 = P1[1]

    lat_list = [lat0]
    lon_list = [lon0]

  #dobijanje tacka odgovarajuce lantitude i longitute u odnosu na intervale
    for i in range(s):
        lat_step = lat0 + interval_lat
        lon_step = lon0 + interval_lon
        lon0 = lon_step
        lat0 = lat_step
        lat_list.append(lat_step)
        lon_list.append(lon_step)

    d_list = []
    for j in range(len(lat_list)):
        lat_p = lat_list[j]
        lon_p = lon_list[j]
        dp = haversine(lat0, lon0, lat_p, lon_p) / 1000  # km
        round(dp)
        d_list.append(dp)

    d_list.reverse()

    #uzimanje nadmorskih visina tacaka izmedju p1 i p2
    elev_list = []
    for j in range(len(lat_list)):
        elev_list.append(get_elevation(lat_list[j], lon_list[j]))

    elev_list.reverse()

    x = d_list  #udaljenost izmedju dve tacke crtamo na x osi
    y = elev_list #nadmorsku visinu tacke crtamo na y osi

    # napomena: grafik je organizovan tako da je druga unesena tacka na distanci nula

    plt.plot(x[0],y[0],'bo', color='red', label='P1')
    #sluzi da predstavimo tacku P2 koja je na nadmorskoj visini y[0]

    plt.plot(x[len(x)-1], y[len(y)-1], 'bo', color='green', label='P2')
    #sluzi da prikazemo polaznu  tacku P1 koja je na udaljenosti od tacke P2 Distance odnosno x[len(x)-1] km
    # a njena nadmorska visina je posledjni element u y listi (y[len(y)-1]) metara

    plt.plot(x, y)
    #ucrtavamo nadmorske visine tacaka koje se nalaze izmedju tacaka P1 i P2

    minimum = min(elev_list)
    for i in range(len(lat_list)):
        plt.fill_between( x[i], minimum, y[i], color="skyblue", alpha=0.2, lw=3)
        #sluzi samo za sencanje oblasti ispod linije grafika

    plt.legend([P2, P1]) #u legendi stoje koordinate zadatih tacaka
    plt.title("Profil terena", loc="center")
    plt.xlabel("Distance: " + str(round(distanca / 1000)) + "km (" + str(round(distanca)) + "m)")
    plt.ylabel("Elevation (m)")

    plt.show()
