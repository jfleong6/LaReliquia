function openTab(event, tabName) {
    document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active-tab"));
    document.querySelectorAll(".tab-content").forEach(content => content.classList.remove("active"));

    event.currentTarget.classList.add("active-tab");
    document.getElementById(tabName).classList.add("active");
}
document.querySelector(".tabs-container").addEventListener("wheel", (event) => {
    event.preventDefault();
    document.querySelector(".tabs-container").scrollLeft += event.deltaY;
});