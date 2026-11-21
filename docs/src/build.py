#!/usr/bin/env python3
"""Genera il sito nelle 4 lingue a partire da src/template.html.

Uso:  python3 src/build.py
Output: index.html (IT), en/index.html, es/index.html, de/index.html
Per cambiare un testo modificalo qui sotto, poi rilancia lo script.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.lifolicasaledicampagna.it/"
LANGS = ["it", "en", "es", "de"]

def tags(*xs):
    return "".join(f"<span>{x}</span>" for x in xs)

T = {}

T["it"] = dict(
    meta_title="Li Fòli – Casale di Campagna | Balaiana, Luogosanto · Gallura, Sardegna",
    meta_desc="Li Fòli è un casale di campagna in granito e calce a Balaiana, Luogosanto, nel cuore della Gallura. Camere e suite immerse tra sughere, rocce di granito e silenzio, vicino alla Costa Smeralda.",
    tagline="Casale di Campagna",
    nav_house="Il Casale", nav_rooms="Camere", nav_nature="Natura", nav_around="Dintorni", nav_book="Prenota",
    cta_avail="Verifica disponibilità", scroll="Scopri",
    intro_eyebrow="Benvenuti a Li Fòli",
    intro_title="Un casale di granito tra le sughere della Gallura",
    intro_lead="Muri di pietra e calce bianca, tetti in coppi, sentieri lastricati che si perdono tra ginestre e buganvillee.",
    intro_p1="Li Fòli è un casale di campagna nella località di Balaiana, nel territorio di Luogosanto, nel cuore più autentico della Gallura. Qui il tempo segue il ritmo della natura: il vento tra gli ulivi selvatici, il volo delle anatre al tramonto, il profumo della macchia mediterranea dopo la pioggia.",
    intro_p2="Le camere sono distribuite tra i volumi bianchi del casale, attorno a una corte interna di prato e granito. Un rifugio silenzioso per chi cerca riposo, a breve distanza dalle spiagge della Costa Smeralda e dell'arcipelago di La Maddalena.",
    alt_hills="Il casale tra le colline della Gallura", alt_bougain="Buganvillea fiorita sul muro di granito",
    f1_t="Natura intatta", f1_d="Sughere secolari, rocce di granito e macchia mediterranea tutt'intorno",
    f2_t="Architettura gallurese", f2_d="Pietra a vista, calce bianca, cotto e travi in legno",
    f3_t="Silenzio e quiete", f3_d="Lontano dal traffico, sotto un cielo pieno di stelle",
    f4_t="Vicino al mare", f4_d="Le spiagge di Palau, Santa Teresa e La Maddalena a portata di mano",
    rooms_eyebrow="Camere &amp; Suite",
    rooms_title="Ogni stanza porta il nome di un fiore della macchia",
    rooms_sub="Ambienti luminosi e curati, arredati con legno, lino e tessuti naturali, con affaccio sul verde della campagna.",
    suite_eyebrow="La Suite",
    suite_desc="La più ampia del casale: soffitto con travi a vista, letto a baldacchino con tende in lino, un salottino con divano e una grande portafinestra aperta sulla campagna gallurese.",
    suite_tags=tags("Letto matrimoniale a baldacchino", "Zona living", "Bagno privato", "Vista campagna"),
    cta_request="Richiedi disponibilità",
    double_room="Camera matrimoniale", photos_soon="Foto in arrivo",
    malva_desc="Toni salvia e cotto, testiera capitonné, specchi d'epoca e una panca in legno ai piedi del letto. Calda, accogliente, luminosa.", photos="foto",
    erica_desc="Dedicata all'erica arborea che colora di bianco le colline galluresi a primavera.",
    euforbia_desc="Travi in ginepro, poltrone in velluto e una portafinestra che si apre sulla corte in pietra. Prende il nome dall'euforbia arborea, che d'inverno accende di giallo i graniti.",
    quote="Dove il granito incontra il cielo, e il silenzio ha il profumo della macchia.",
    nature_eyebrow="Il casale e la natura attorno",
    nature_title="Sughere, granito e sentieri da esplorare",
    nature_p="Il casale è circondato da boschi di sughere secolari, muretti a secco e formazioni di granito modellate dal vento. Un paesaggio da vivere a piedi o in bicicletta, tra passaggi nascosti nella roccia e radure dove al tramonto volano le anatre selvatiche.",
    cap_pool="La piscina tra i graniti", cap_court="La corte interna", cap_granite="Granito scolpito dal vento",
    cap_cork="Sughere e muretti a secco", cap_moon="Il casale con la luna", cap_water="Acqua cristallina",
    cap_hill="Ai piedi della collina", cap_rocks="Passaggi tra le rocce",
    around_eyebrow="Dintorni", around_title="Il cuore della Gallura, tra borghi e mare",
    around_sub="Da Li Fòli si raggiungono facilmente alcune delle mete più belle del nord Sardegna. <em>(Tempi indicativi in auto.)</em>",
    d_few="Pochi minuti",
    p_luogo="Il borgo delle chiese campestri: la Basilica di Nostra Signora di Luogosanto, l'eremo di San Trano scavato nella roccia e il Palazzo di Baldu.",
    p_palau="Il traghetto per l'arcipelago, le spiagge di Porto Pollo e Capo d'Orso, il mare cristallino delle isole.",
    p_steresa="Capo Testa, la Valle della Luna e la spiaggia di Rena Bianca affacciata sulle Bocche di Bonifacio.",
    p_tempio="Il centro storico in granito, le sorgenti di Rinaggiu e il Monte Limbara per escursioni panoramiche.",
    p_costa="Porto Cervo, Baja Sardinia e le calette più famose della Sardegna.",
    p_olbia="Aeroporto e porto: il punto di arrivo ideale per raggiungere il casale.",
    contact_eyebrow="Contatti &amp; prenotazioni", contact_title="Vieni a trovarci",
    contact_p="Scrivici per verificare la disponibilità, chiedere un preventivo o qualsiasi informazione sul soggiorno. Ti risponderemo il prima possibile.",
    sardinia="Sardegna", phone="Telefono / WhatsApp", tbd="da inserire",
    form_title="Richiesta di disponibilità", f_name="Nome", f_name_ph="Il tuo nome",
    f_in="Arrivo", f_out="Partenza", f_guests="Ospiti", f_room="Camera", f_nopref="Nessuna preferenza",
    f_msg="Messaggio", f_msg_ph="Richieste particolari, orario di arrivo…", f_send="Invia richiesta",
)

T["en"] = dict(
    meta_title="Li Fòli – Country Retreat | Balaiana, Luogosanto · Gallura, Sardinia",
    meta_desc="Li Fòli is a granite-and-lime country house in Balaiana, Luogosanto, in the heart of Gallura, Sardinia. Rooms and a suite surrounded by cork oaks, granite boulders and silence, close to the Costa Smeralda.",
    tagline="Country Retreat",
    nav_house="The House", nav_rooms="Rooms", nav_nature="Nature", nav_around="Surroundings", nav_book="Book",
    cta_avail="Check availability", scroll="Discover",
    intro_eyebrow="Welcome to Li Fòli",
    intro_title="A granite farmhouse among the cork oaks of Gallura",
    intro_lead="Stone walls and white lime, terracotta-tiled roofs, paved paths winding through broom and bougainvillea.",
    intro_p1="Li Fòli is a country house in Balaiana, in the countryside of Luogosanto, in the most authentic heart of Gallura. Here time follows the rhythm of nature: the wind in the wild olive trees, ducks flying at sunset, the scent of the Mediterranean scrub after the rain.",
    intro_p2="The rooms are spread across the white buildings of the farmhouse, around an inner courtyard of lawn and granite. A quiet retreat for those seeking rest, a short drive from the beaches of the Costa Smeralda and the La Maddalena archipelago.",
    alt_hills="The farmhouse among the hills of Gallura", alt_bougain="Bougainvillea in bloom on a granite wall",
    f1_t="Unspoilt nature", f1_d="Centuries-old cork oaks, granite boulders and Mediterranean scrub all around",
    f2_t="Gallurese architecture", f2_d="Exposed stone, white lime, terracotta and wooden beams",
    f3_t="Peace and quiet", f3_d="Far from traffic, under a sky full of stars",
    f4_t="Close to the sea", f4_d="The beaches of Palau, Santa Teresa and La Maddalena within easy reach",
    rooms_eyebrow="Rooms &amp; Suite",
    rooms_title="Every room is named after a flower of the maquis",
    rooms_sub="Bright, carefully designed rooms furnished with wood, linen and natural fabrics, overlooking the green countryside.",
    suite_eyebrow="The Suite",
    suite_desc="The largest room in the house: a beamed ceiling, a canopy bed with linen curtains, a small sitting area with a sofa and a large French window opening onto the Gallura countryside.",
    suite_tags=tags("Double canopy bed", "Living area", "Private bathroom", "Countryside view"),
    cta_request="Request availability",
    double_room="Double room", photos_soon="Photos coming soon",
    malva_desc="Sage and terracotta tones, a tufted headboard, vintage mirrors and a wooden bench at the foot of the bed. Warm, welcoming and bright.", photos="photos",
    erica_desc="Named after the tree heath that paints the hills of Gallura white in spring.",
    euforbia_desc="Juniper beams, velvet wingback armchairs and a French window opening onto the stone courtyard. Named after the tree spurge, which lights up the granite with yellow in winter.",
    quote="Where granite meets the sky, and silence smells of the maquis.",
    nature_eyebrow="The house and the nature around it",
    nature_title="Cork oaks, granite and trails to explore",
    nature_p="The house is surrounded by centuries-old cork oak woods, dry-stone walls and wind-sculpted granite formations. A landscape to explore on foot or by bike, through hidden passages in the rock and clearings where wild ducks fly at sunset.",
    cap_pool="The pool among the granite", cap_court="The inner courtyard", cap_granite="Wind-sculpted granite",
    cap_cork="Cork oaks and dry-stone walls", cap_moon="The house under the moon", cap_water="Crystal-clear water",
    cap_hill="At the foot of the hill", cap_rocks="Passages through the rocks",
    around_eyebrow="Surroundings", around_title="The heart of Gallura, between villages and sea",
    around_sub="From Li Fòli you can easily reach some of the most beautiful places in northern Sardinia. <em>(Approximate driving times.)</em>",
    d_few="A few minutes",
    p_luogo="The village of country churches: the Basilica of Our Lady of Luogosanto, the hermitage of San Trano carved into the rock and the Palazzo di Baldu.",
    p_palau="Ferries to the archipelago, the beaches of Porto Pollo and Capo d'Orso, and the crystal-clear waters of the islands.",
    p_steresa="Capo Testa, the Valle della Luna and Rena Bianca beach overlooking the Strait of Bonifacio.",
    p_tempio="The granite old town, the Rinaggiu springs and Monte Limbara for panoramic hikes.",
    p_costa="Porto Cervo, Baja Sardinia and the most famous coves in Sardinia.",
    p_olbia="Airport and port: the ideal arrival point to reach the house.",
    contact_eyebrow="Contact &amp; bookings", contact_title="Come and visit us",
    contact_p="Write to us to check availability, ask for a quote or any information about your stay. We will get back to you as soon as possible.",
    sardinia="Sardinia, Italy", phone="Phone / WhatsApp", tbd="coming soon",
    form_title="Availability request", f_name="Name", f_name_ph="Your name",
    f_in="Arrival", f_out="Departure", f_guests="Guests", f_room="Room", f_nopref="No preference",
    f_msg="Message", f_msg_ph="Special requests, arrival time…", f_send="Send request",
)

T["es"] = dict(
    meta_title="Li Fòli – Casa rural | Balaiana, Luogosanto · Gallura, Cerdeña",
    meta_desc="Li Fòli es una casa rural de granito y cal en Balaiana, Luogosanto, en el corazón de la Gallura, Cerdeña. Habitaciones y una suite rodeadas de alcornoques, rocas de granito y silencio, cerca de la Costa Esmeralda.",
    tagline="Casa Rural",
    nav_house="La Casa", nav_rooms="Habitaciones", nav_nature="Naturaleza", nav_around="Alrededores", nav_book="Reservar",
    cta_avail="Consultar disponibilidad", scroll="Descubrir",
    intro_eyebrow="Bienvenidos a Li Fòli",
    intro_title="Una casa de granito entre los alcornoques de la Gallura",
    intro_lead="Muros de piedra y cal blanca, tejados de teja árabe, senderos empedrados que se pierden entre retamas y buganvillas.",
    intro_p1="Li Fòli es una casa rural en la localidad de Balaiana, en el término de Luogosanto, en el corazón más auténtico de la Gallura. Aquí el tiempo sigue el ritmo de la naturaleza: el viento entre los acebuches, el vuelo de los patos al atardecer, el aroma del monte mediterráneo después de la lluvia.",
    intro_p2="Las habitaciones se reparten entre los volúmenes blancos de la casa, alrededor de un patio interior de césped y granito. Un refugio tranquilo para quien busca descanso, a poca distancia de las playas de la Costa Esmeralda y del archipiélago de La Maddalena.",
    alt_hills="La casa entre las colinas de la Gallura", alt_bougain="Buganvilla en flor sobre un muro de granito",
    f1_t="Naturaleza intacta", f1_d="Alcornoques centenarios, rocas de granito y monte mediterráneo por todas partes",
    f2_t="Arquitectura gallurense", f2_d="Piedra vista, cal blanca, barro cocido y vigas de madera",
    f3_t="Silencio y calma", f3_d="Lejos del tráfico, bajo un cielo lleno de estrellas",
    f4_t="Cerca del mar", f4_d="Las playas de Palau, Santa Teresa y La Maddalena al alcance de la mano",
    rooms_eyebrow="Habitaciones &amp; Suite",
    rooms_title="Cada habitación lleva el nombre de una flor del monte",
    rooms_sub="Espacios luminosos y cuidados, decorados con madera, lino y tejidos naturales, con vistas al verde del campo.",
    suite_eyebrow="La Suite",
    suite_desc="La más amplia de la casa: techo con vigas vistas, cama con dosel y cortinas de lino, una pequeña sala de estar con sofá y un gran ventanal abierto al campo de la Gallura.",
    suite_tags=tags("Cama doble con dosel", "Zona de estar", "Baño privado", "Vistas al campo"),
    cta_request="Solicitar disponibilidad",
    double_room="Habitación doble", photos_soon="Fotos próximamente",
    malva_desc="Tonos salvia y terracota, cabecero capitoné, espejos antiguos y un banco de madera a los pies de la cama. Cálida, acogedora y luminosa.", photos="fotos",
    erica_desc="Dedicada al brezo blanco que tiñe de blanco las colinas de la Gallura en primavera.",
    euforbia_desc="Vigas de enebro, butacas de terciopelo y un ventanal que se abre al patio de piedra. Debe su nombre a la euforbia arbórea, que en invierno enciende de amarillo los granitos.",
    quote="Donde el granito se encuentra con el cielo, y el silencio huele a monte mediterráneo.",
    nature_eyebrow="La casa y la naturaleza que la rodea",
    nature_title="Alcornoques, granito y senderos por explorar",
    nature_p="La casa está rodeada de bosques de alcornoques centenarios, muros de piedra seca y formaciones de granito moldeadas por el viento. Un paisaje para recorrer a pie o en bicicleta, entre pasajes escondidos en la roca y claros donde al atardecer vuelan los patos salvajes.",
    cap_pool="La piscina entre los granitos", cap_court="El patio interior", cap_granite="Granito esculpido por el viento",
    cap_cork="Alcornoques y muros de piedra seca", cap_moon="La casa bajo la luna", cap_water="Agua cristalina",
    cap_hill="Al pie de la colina", cap_rocks="Pasajes entre las rocas",
    around_eyebrow="Alrededores", around_title="El corazón de la Gallura, entre pueblos y mar",
    around_sub="Desde Li Fòli se llega fácilmente a algunos de los lugares más bonitos del norte de Cerdeña. <em>(Tiempos aproximados en coche.)</em>",
    d_few="Pocos minutos",
    p_luogo="El pueblo de las iglesias rurales: la Basílica de Nuestra Señora de Luogosanto, la ermita de San Trano excavada en la roca y el Palazzo di Baldu.",
    p_palau="El ferry al archipiélago, las playas de Porto Pollo y Capo d'Orso y el mar cristalino de las islas.",
    p_steresa="Capo Testa, el Valle della Luna y la playa de Rena Bianca frente a las Bocas de Bonifacio.",
    p_tempio="El casco antiguo de granito, los manantiales de Rinaggiu y el Monte Limbara para excursiones panorámicas.",
    p_costa="Porto Cervo, Baja Sardinia y las calas más famosas de Cerdeña.",
    p_olbia="Aeropuerto y puerto: el punto de llegada ideal para llegar a la casa.",
    contact_eyebrow="Contacto &amp; reservas", contact_title="Ven a visitarnos",
    contact_p="Escríbenos para consultar la disponibilidad, pedir un presupuesto o cualquier información sobre tu estancia. Te responderemos lo antes posible.",
    sardinia="Cerdeña, Italia", phone="Teléfono / WhatsApp", tbd="próximamente",
    form_title="Solicitud de disponibilidad", f_name="Nombre", f_name_ph="Tu nombre",
    f_in="Llegada", f_out="Salida", f_guests="Huéspedes", f_room="Habitación", f_nopref="Sin preferencia",
    f_msg="Mensaje", f_msg_ph="Peticiones especiales, hora de llegada…", f_send="Enviar solicitud",
)

T["de"] = dict(
    meta_title="Li Fòli – Landhaus | Balaiana, Luogosanto · Gallura, Sardinien",
    meta_desc="Li Fòli ist ein Landhaus aus Granit und Kalk in Balaiana, Luogosanto, im Herzen der Gallura auf Sardinien. Zimmer und eine Suite inmitten von Korkeichen, Granitfelsen und Stille, nahe der Costa Smeralda.",
    tagline="Landhaus",
    nav_house="Das Haus", nav_rooms="Zimmer", nav_nature="Natur", nav_around="Umgebung", nav_book="Buchen",
    cta_avail="Verfügbarkeit prüfen", scroll="Entdecken",
    intro_eyebrow="Willkommen in Li Fòli",
    intro_title="Ein Granit-Landhaus zwischen den Korkeichen der Gallura",
    intro_lead="Steinmauern und weißer Kalk, Dächer aus Tonziegeln, gepflasterte Wege zwischen Ginster und Bougainvillea.",
    intro_p1="Li Fòli ist ein Landhaus im Ortsteil Balaiana, in der Gemeinde Luogosanto, im ursprünglichsten Herzen der Gallura. Hier folgt die Zeit dem Rhythmus der Natur: der Wind in den wilden Olivenbäumen, Enten, die bei Sonnenuntergang fliegen, der Duft der Macchia nach dem Regen.",
    intro_p2="Die Zimmer verteilen sich auf die weißen Gebäude des Landhauses, rund um einen Innenhof aus Rasen und Granit. Ein ruhiger Rückzugsort für alle, die Erholung suchen – nur eine kurze Fahrt von den Stränden der Costa Smeralda und dem La-Maddalena-Archipel entfernt.",
    alt_hills="Das Landhaus zwischen den Hügeln der Gallura", alt_bougain="Blühende Bougainvillea an einer Granitmauer",
    f1_t="Unberührte Natur", f1_d="Jahrhundertealte Korkeichen, Granitfelsen und Macchia ringsum",
    f2_t="Galluresische Architektur", f2_d="Sichtstein, weißer Kalk, Terrakotta und Holzbalken",
    f3_t="Stille und Ruhe", f3_d="Fernab vom Verkehr, unter einem Himmel voller Sterne",
    f4_t="Nah am Meer", f4_d="Die Strände von Palau, Santa Teresa und La Maddalena in greifbarer Nähe",
    rooms_eyebrow="Zimmer &amp; Suite",
    rooms_title="Jedes Zimmer trägt den Namen einer Blume der Macchia",
    rooms_sub="Helle, liebevoll gestaltete Räume mit Holz, Leinen und Naturstoffen und Blick ins Grüne.",
    suite_eyebrow="Die Suite",
    suite_desc="Das größte Zimmer des Hauses: sichtbare Holzbalken, ein Himmelbett mit Leinenvorhängen, eine kleine Sitzecke mit Sofa und eine große Fenstertür mit Blick auf die Landschaft der Gallura.",
    suite_tags=tags("Doppel-Himmelbett", "Wohnbereich", "Eigenes Bad", "Blick ins Grüne"),
    cta_request="Verfügbarkeit anfragen",
    double_room="Doppelzimmer", photos_soon="Fotos folgen",
    malva_desc="Salbei- und Terrakottatöne, ein Chesterfield-Kopfteil, antike Spiegel und eine Holzbank am Fußende des Bettes. Warm, einladend und hell.", photos="Fotos",
    erica_desc="Benannt nach der Baumheide, die im Frühling die Hügel der Gallura weiß färbt.",
    euforbia_desc="Wacholderbalken, Ohrensessel aus Samt und eine Fenstertür zum steinernen Innenhof. Benannt nach der Baum-Wolfsmilch, die im Winter den Granit gelb leuchten lässt.",
    quote="Wo Granit auf Himmel trifft und die Stille nach Macchia duftet.",
    nature_eyebrow="Das Haus und die Natur ringsum",
    nature_title="Korkeichen, Granit und Wege zum Entdecken",
    nature_p="Das Haus ist umgeben von jahrhundertealten Korkeichenwäldern, Trockenmauern und vom Wind geformten Granitfelsen. Eine Landschaft, die man zu Fuß oder mit dem Fahrrad erleben kann – durch versteckte Felsdurchgänge und über Lichtungen, über denen bei Sonnenuntergang Wildenten fliegen.",
    cap_pool="Der Pool zwischen Granitfelsen", cap_court="Der Innenhof", cap_granite="Vom Wind geformter Granit",
    cap_cork="Korkeichen und Trockenmauern", cap_moon="Das Haus im Mondlicht", cap_water="Kristallklares Wasser",
    cap_hill="Am Fuß des Hügels", cap_rocks="Durchgänge zwischen den Felsen",
    around_eyebrow="Umgebung", around_title="Das Herz der Gallura, zwischen Dörfern und Meer",
    around_sub="Von Li Fòli aus erreichen Sie bequem einige der schönsten Orte im Norden Sardiniens. <em>(Ungefähre Fahrzeiten mit dem Auto.)</em>",
    d_few="Wenige Minuten",
    p_luogo="Das Dorf der Landkirchen: die Basilika Nostra Signora di Luogosanto, die in den Fels gehauene Einsiedelei San Trano und der Palazzo di Baldu.",
    p_palau="Die Fähre zum Archipel, die Strände von Porto Pollo und Capo d'Orso und das kristallklare Wasser der Inseln.",
    p_steresa="Capo Testa, das Valle della Luna und der Strand Rena Bianca mit Blick auf die Straße von Bonifacio.",
    p_tempio="Die Altstadt aus Granit, die Quellen von Rinaggiu und der Monte Limbara für Panoramawanderungen.",
    p_costa="Porto Cervo, Baja Sardinia und die berühmtesten Buchten Sardiniens.",
    p_olbia="Flughafen und Hafen: der ideale Ankunftsort für die Anreise zum Haus.",
    contact_eyebrow="Kontakt &amp; Buchung", contact_title="Besuchen Sie uns",
    contact_p="Schreiben Sie uns, um die Verfügbarkeit zu prüfen, ein Angebot anzufragen oder Informationen zu Ihrem Aufenthalt zu erhalten. Wir antworten Ihnen so schnell wie möglich.",
    sardinia="Sardinien, Italien", phone="Telefon / WhatsApp", tbd="folgt",
    form_title="Verfügbarkeitsanfrage", f_name="Name", f_name_ph="Ihr Name",
    f_in="Anreise", f_out="Abreise", f_guests="Gäste", f_room="Zimmer", f_nopref="Keine Präferenz",
    f_msg="Nachricht", f_msg_ph="Besondere Wünsche, Ankunftszeit…", f_send="Anfrage senden",
)

def build():
    tpl = open(os.path.join(ROOT, "src", "template.html"), encoding="utf-8").read()
    keys = set(re.findall(r"\{\{(\w+)\}\}", tpl)) - {"lang", "B", "hreflang", "langlinks"}
    for lang in LANGS:
        missing = keys - set(T[lang])
        assert not missing, f"{lang}: mancano le chiavi {sorted(missing)}"
        base = "" if lang == "it" else "../"
        hreflang = "\n".join(
            f'<link rel="alternate" hreflang="{l}" href="{SITE}{"" if l == "it" else l + "/"}">' for l in LANGS
        ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}">'
        links = "".join(
            f'<a href="{base}{"" if l == "it" else l + "/"}index.html" data-l="{l}" class="{"on" if l == lang else ""}" hreflang="{l}">{l.upper()}</a>'
            for l in LANGS
        )
        out = tpl
        for k, v in {**T[lang], "lang": lang, "B": base, "hreflang": hreflang, "langlinks": links}.items():
            out = out.replace("{{" + k + "}}", v)
        assert "{{" not in out, f"{lang}: segnaposto non sostituiti"
        path = os.path.join(ROOT, "index.html") if lang == "it" else os.path.join(ROOT, lang, "index.html")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(out)
        print("ok", os.path.relpath(path, ROOT))

if __name__ == "__main__":
    build()
