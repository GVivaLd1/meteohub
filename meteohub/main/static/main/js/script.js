const sideBarButton = document.querySelector("#toggle-sidebar-btn");
const cityInput = document.querySelector("#city-input");
const citySearchButton = document.querySelector("#city-search");
const historyBlock = document.querySelector(".search-history");
const cityHeader = document.querySelector("#city-header");
const summaryBlock = document.querySelector("#summary");
const searchBlock = document.querySelector("#search-block");
const searchLabel = document.querySelector("label");
const statsWrapper = document.querySelector("#stats-wrapper");
const forecastWrapper = document.querySelector("#forecast-wrapper");
const historyWrapper = document.querySelector("#history-wrapper");

const rawDaysDATA = document.querySelector("#days-stats").textContent;
let daysData = JSON.parse(rawDaysDATA);
let generalData = null;

const maxHistoryLenth = 5;

let history = getSearchHistory();
let currentOpenDate = null;

renderHistory();

function getSearchHistory() {
    const history = localStorage.getItem("weather_search_history");
    return history ? JSON.parse(history) : [];
}

function addToHistory(cityName) {

    let history = getSearchHistory();
    history = history.filter(city => city.toLowerCase() !== cityName.toLowerCase());

    history.unshift(cityName);

    if (history.length > maxHistoryLenth) {
        history.pop();
    }

    localStorage.setItem("weather_search_history", JSON.stringify(history));
    renderHistory();
}

async function fetchWeatherData(cityName) {
    try{
        const response = await fetch(`/api/weather/?city=${encodeURIComponent(cityName)}`);

        if (!response.ok) {
                throw new Error(`Помилка сервера: ${response.status}`);
            }

        const responseData = await response.json();

        daysData = responseData.days_statistics;
        generalData = responseData.general_statistics;
            
        forecastWrapper.innerHTML = responseData.days_html;

        if (summaryBlock.classList.contains("initial-state")) {
            summaryBlock.classList.remove("initial-state");
            searchBlock.classList.add("weather-found");

            statsWrapper.style.display = "contents";
            forecastWrapper.style.display = "contents";
            historyWrapper.style.display = "contents";

            searchLabel.textContent = "Пошук міста";
        }

        if (currentOpenDate !== null) {
            renderDaysStats(currentOpenDate);
        }
        else{
            renderGeneralStats();
        }

        const daysBlock = document.querySelector(".days-of-week");
        daysBlock.addEventListener("click", (event) => {
            const clickedEl = event.target.closest("div");
            if (!clickedEl || !clickedEl.classList.contains("day-name")) return;

            renderDaysStats(clickedEl.dataset.date);
        });
    }
    catch (error) {
        console.log(`Помилка: ${error}`);
    }
}

function renderHistory() {
    const history = getSearchHistory();

    historyBlock.innerHTML = "";

    history.forEach(city => {
        li = document.createElement("li");

        li.className = "history-element";
        li.textContent = city;

        historyBlock.appendChild(li);
    });
}

function renderDaysStats(date) {
    const chosenDayDATA = daysData[date];

    if (!chosenDayDATA) {
        renderGeneralStats();
        return;
    }

    statsWrapper.innerHTML = `
                    <div id="table-statistics">
                        <div id="stats-head">
                            <h3>Статистика за ${date}</h3>
                            <button>X</button>
                        </div>
                        <div id="stats-body-day">

                            <h4>Температура</h4>
                            <div class="stats-type">
                                
                                <div class="stat-card">
                                    <span class="stat-name">Максимальна</span>
                                    <span class="stat-content">${chosenDayDATA.highest_temp[0]}</span>
                                    <span class="stat-source">${chosenDayDATA.highest_temp[1]}</span>
                                </div>

                                <div class="stat-card">
                                    <span class="stat-name">Мінімальна</span>
                                    <span class="stat-content">${chosenDayDATA.lowest_temp[0]}</span>
                                    <span class="stat-source">${chosenDayDATA.lowest_temp[1]}</span>
                                </div>

                                <div class="stat-card">
                                    <span class="stat-name">Середня максимальна</span>
                                    <span class="stat-content">${chosenDayDATA.avg_max}</span>
                                </div>

                                <div class="stat-card">
                                    <span class="stat-name">Середня мінімальна</span>
                                    <span class="stat-content">${chosenDayDATA.avg_min}</span>
                                </div>
                            </div>

                            <h4>Погода</h4>
                            <div class="stats-type">

                                <div class="stat-card">
                                    <span class="stat-name">Найчастіша</span>
                                    <span class="stat-content">${chosenDayDATA.most_frequent_condition}</span>
                                </div>

                                <div class="stat-card">
                                    <span class="stat-name">Найрідкісніша</span>
                                    <span class="stat-content">${chosenDayDATA.least_frequent_condition}</span>
                                </div>
                            </div>

                        </div>
                    </div>`;

    const exitBtn = statsWrapper.querySelector("button");

    exitBtn.addEventListener("click", () => {
        renderGeneralStats();
    });
}

function renderGeneralStats() {
    currentOpenDate = null;
    statsWrapper.innerHTML = `
                    <div id="table-statistics">
                        <div id="stats-head">
                            <h3>Загальна статистика</h3>
                        </div>
                        <div id="stats-body-general">

                            <div class="stat-card">
                                <span class="stat-name">Максимальна температура</span>
                                <span class="stat-content">${generalData.highest_temp[0]}</span>
                                <span class="stat-source">${generalData.highest_temp[1]}</span>
                            </div>

                            <div class="stat-card">
                                <span class="stat-name">Мінімальна температура</span>
                                <span class="stat-content">${generalData.lowest_temp[0]}</span>
                                <span class="stat-source">${generalData.lowest_temp[1]}</span>
                            </div>

                            <div class="stat-card">
                                <span class="stat-name">Найчастіша погода</span>
                                <span class="stat-content">${generalData.most_frequent_condition}</span>
                            </div>

                            <div class="stat-card">
                                <span class="stat-name">Найрідкісніша погода</span>
                                <span class="stat-content">${generalData.least_frequent_condition}</span>
                            </div>
                        </div>
                    </div>`;
}

sideBarButton.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("collapsed");
});

citySearchButton.addEventListener("click", () => {
    const cityName = cityInput.value.trim();
    if (!cityName) return;

    addToHistory(cityName);
    fetchWeatherData(cityName);
});

cityInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        const cityName = cityInput.value.trim();
        if (!cityName) return;

        addToHistory(cityName);
        fetchWeatherData(cityName);
    }
});

historyBlock.addEventListener("click", (event) => {
    const clickedItem = event.target;
    const ItemContent = clickedItem.textContent;

    fetchWeatherData(ItemContent);
    addToHistory(ItemContent);
});