const img = document.getElementById("img"),
    prev = document.getElementById("prev"),
    dropText = document.getElementById("dropText");

const go = document.getElementById("go"),
    loc = document.getElementById("loc"),
    locText = document.getElementById("locText");

let coords = { lat: null, lon: null };

img.onchange = () => {
    let f = img.files[0];
    if (!f) return;

    prev.src = URL.createObjectURL(f);
    prev.style.display = "block";
    dropText.style.display = "none";
    go.disabled = false;
};

loc.onclick = () =>
    navigator.geolocation.getCurrentPosition(
        p => {
            coords = {
                lat: p.coords.latitude,
                lon: p.coords.longitude
            };

            locText.textContent = "📍 Location ready";
            loadWeather();
        },
        () => {
            locText.textContent =
                "Location unavailable; demo weather will be used.";
        }
    );

async function loadWeather() {
    let u = coords.lat
        ? `/api/weather?lat=${coords.lat}&lon=${coords.lon}`
        : "/api/weather";

    let r = await fetch(u);

    if (!r.ok) return;

    renderWeather(await r.json());
}

function renderWeather(d) {
    let c = d.current || {};

    document.getElementById("temp").textContent =
        Math.round(c.temperature || 0);

    document.getElementById("hum").textContent =
        Math.round(c.humidity || 0);

    document.getElementById("rp").textContent =
        Math.round(c.rain_probability || 0);

    let b = document.getElementById("bars");

    b.innerHTML = "";

    (d.hourly || [])
        .slice(0, 12)
        .forEach(x => {
            let e = document.createElement("div");

            e.className =
                "bar" + (x.rain_probability >= 60 ? " high" : "");

            e.style.height =
                Math.max(5, (x.rain_probability || 0) * 1.5) + "px";

            b.appendChild(e);
        });
}

loadWeather();

go.onclick = async () => {
    let fd = new FormData();

    fd.append("image", img.files[0]);

    fd.append(
        "crop",
        document.getElementById("crop").value
    );

    if (coords.lat) {
        fd.append("lat", coords.lat);
        fd.append("lon", coords.lon);
    }

    document.getElementById("status").textContent =
        "Analyzing…";

    go.disabled = true;

    try {
        let r = await fetch("/api/analyze", {
            method: "POST",
            body: fd
        });

        let d = await r.json();

        if (!r.ok)
            throw Error(d.error);

        render(d);

        document
            .getElementById("result")
            .classList.remove("hidden");

        document
            .getElementById("result")
            .scrollIntoView({
                behavior: "smooth"
            });

    } catch (e) {
        alert(e.message);

    } finally {
        go.disabled = false;

        document.getElementById("status").textContent = "";
    }
};


function render(d) {

    // Prevent "Cannot read properties of undefined"
    // when backend does not return prediction.
    if (!d || !d.prediction) {
        throw new Error(
            d?.error ||
            "Backend returned an invalid analysis response: prediction is missing."
        );
    }

    let p = d.prediction,
        s = d.decision,
        g = d.guidance;

    document.getElementById("title").textContent =
        p.crop + " field report";

    document.getElementById("mode").textContent =
        p.mode.toUpperCase();

    document.getElementById("rimg").src =
        d.image_url;

    document.getElementById("disease").textContent =
        p.disease;

    document.getElementById("conf").textContent =
        p.confidence + "%";

    document.getElementById("confbar").style.width =
        p.confidence + "%";

    document.getElementById("ev").innerHTML =
        (p.evidence || [])
            .map(x => `<p>✓ ${x}</p>`)
            .join("");

    let icons = {
        ACT: "🟢",
        CAUTION: "🟡",
        WAIT: "🔴",
        VERIFY: "⚠️"
    };

    document.getElementById("icon").textContent =
        icons[s.action] || "🧭";

    document.getElementById("headline").textContent =
        s.headline;

    document.getElementById("msg").textContent =
        d.farmer_message;

    document.getElementById("score").textContent =
        s.score + "%";

    document.getElementById("scorebar").style.width =
        s.score + "%";

    document.getElementById("window").textContent =
        s.next_window
            ? "Next suitable window: " +
              new Date(
                  s.next_window.start
              ).toLocaleString() +
              " · rain " +
              s.next_window.rain_probability +
              "%"
            : "No suitable window found in forecast.";

    document.getElementById("reasons").innerHTML =
        (s.reasons || [])
            .map(x => `<div class="reason">• ${x}</div>`)
            .join("");

    document.getElementById("gname").textContent =
        g.name;

    document.getElementById("gsummary").textContent =
        g.summary;

    document.getElementById("manage").innerHTML =
        (g.management || [])
            .map(x => `<li>${x}</li>`)
            .join("");

    document.getElementById("safety").textContent =
        "⚠️ " + g.safety;

    document.getElementById("dr").textContent =
        d.climate_risk.disease_pressure;

    document.getElementById("hr").textContent =
        d.climate_risk.heat_stress;

    document.getElementById("or").textContent =
        d.climate_risk.overall;
}


let lastMessage = "";

document.getElementById("speak").onclick = () => {

    if (!lastMessage) return;

    let u =
        new SpeechSynthesisUtterance(lastMessage);

    u.lang = "te-IN";

    speechSynthesis.cancel();

    speechSynthesis.speak(u);
};


document.getElementById("lang").onclick = () => {

    document.getElementById("lang").textContent =
        document.getElementById("lang").textContent ===
        "తెలుగు"
            ? "English"
            : "తెలుగు";
};


const oldRender = render;

render = function (d) {

    oldRender(d);

    lastMessage =
        d.farmer_message || "";

    document.getElementById("telugu").textContent =
        d.farmer_message || "";

    document.getElementById("sources").innerHTML =
        (d.sources || [])
            .map(
                s =>
                    `<a target="_blank" rel="noopener" href="${s.url}">
                        ↗ ${s.title}
                    </a>`
            )
            .join("<br>") ||
        "No source mapping available.";
};