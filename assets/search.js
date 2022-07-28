function init() {
  const names = Array.from(document.querySelectorAll(".name"));
  const descriptions = Array.from(document.querySelectorAll(".description"));
  const searchables = [...names, ...descriptions];
  const searchField = document.querySelector(".search");
  const cards = Array.from(document.querySelectorAll(".card"));

  const show = (cards) => cards.forEach((c) => c.classList.remove("hidden"));
  const hide = (cards) => cards.forEach((c) => c.classList.add("hidden"));

  searchField.addEventListener("keyup", (e) => {
    const searchTerm = e.target.value.toLowerCase();

    if (searchTerm) {
      hide(cards);

      const matchingCards = searchables.reduce((arr, i) => {
        if (i.innerText.toLowerCase().includes(searchTerm))
          arr.push(i.parentElement);
        return arr;
      }, []);

      show(matchingCards);
    } else {
      show(cards);
    }
  });
}
