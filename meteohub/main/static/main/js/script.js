const sideBarButton = document.querySelector("#toggle-sidebar-btn");
const daysBlock = document.querySelector(".days-of-week");
const tableStatsBlock = document.querySelector("#table-statistics");

const rawDaysDATA = document.querySelector("#days-stats").textContent;
const daysDATA = JSON.parse(rawDaysDATA);

const generalStats = tableStatsBlock.innerHTML;

sideBarButton.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("collapsed");
});

daysBlock.addEventListener("click", (event) => {
    const clickedEl = event.target.closest("div");
    if (!clickedEl || !clickedEl.classList.contains("day-name")) return;

    chosenDayDATA = daysDATA[clickedEl.dataset.date];
    
    tableStatsBlock.innerHTML = 
                        `<div id="stats-head">
                            <h1>Статистика за ${clickedEl.dataset.date}</h1>
                            <button>X</button>
                        </div>
                        <div id="stats-body-day">

                            <h2>Температура</h2>
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

                            <h2>Погода</h2>
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

                        </div>`

    const exitBtn = tableStatsBlock.querySelector("button");

    exitBtn.addEventListener("click", () => {
        tableStatsBlock.innerHTML = generalStats;
    });
});