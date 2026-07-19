const sideBarButton = document.querySelector("#toggle-sidebar-btn");
const daysBlock = document.querySelector(".days-of-week");
const tableStatsBlock = document.querySelector("#table-statistics");
const cityInput = document.querySelector("#city-input");
const citySearchButton = document.querySelector("#city-search");
const historyBlock = document.querySelector(".search-history");
const cityHeader = document.querySelector("#city-header");
const cardsContainer = document.querySelector("#cards-container");

const rawDaysDATA = document.querySelector("#days-stats").textContent;
let daysDATA = JSON.parse(rawDaysDATA);

const generalStats = tableStatsBlock.innerHTML;

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

        daysDATA = responseData.days_statistics;
            
            cityHeader.textContent = `Прогнози для міста ${responseData.city_name}`;
            cardsContainer.innerHTML = responseData.days_html;

            if (currentOpenDate !== null) {
                renderDaysStats(currentOpenDate);
            }
            else{
                renderGeneralStats(responseData.general_statistics);
            }
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
    chosenDayDATA = daysDATA[date];

    if (!chosenDayDATA) {
        renderGeneralStats();
        return;
    }

    tableStatsBlock.innerHTML = 
                        `<div id="stats-head">
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

                        </div>`;

    const exitBtn = tableStatsBlock.querySelector("button");

    exitBtn.addEventListener("click", () => {
        renderGeneralStats();
    });
}

function renderGeneralStats(data) {
    currentOpenDate = null;
    tableStatsBlock.innerHTML = `<div id="stats-head">
                            <h3>Загальна статистика</h3>
                        </div>
                        <div id="stats-body-general">

                            <div class="stat-card">
                                <span class="stat-name">Максимальна температура</span>
                                <span class="stat-content">${data.highest_temp[0]}</span>
                                <span class="stat-source">${data.highest_temp[1]}</span>
                            </div>

                            <div class="stat-card">
                                <span class="stat-name">Мінімальна температура</span>
                                <span class="stat-content">${data.lowest_temp[0]}</span>
                                <span class="stat-source">${data.lowest_temp[1]}</span>
                            </div>

                            <div class="stat-card">
                                <span class="stat-name">Найчастіша погода</span>
                                <span class="stat-content">${data.most_frequent_condition}</span>
                            </div>

                            <div class="stat-card">
                                <span class="stat-name">Найрідкісніша погода</span>
                                <span class="stat-content">${data.least_frequent_condition}</span>
                            </div>
                        </div>`;
}

sideBarButton.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("collapsed");
});

daysBlock.addEventListener("click", (event) => {
    const clickedEl = event.target.closest("div");
    if (!clickedEl || !clickedEl.classList.contains("day-name")) return;

    renderDaysStats(clickedEl.dataset.date);
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