const base = 'data/processed/';
const trend = document.querySelector('#trend');

async function showAdvisoryExplorer() {
  const container = document.querySelector('#advisory-explorer');
  const select = document.querySelector('#warning-type');
  try {
    const records = await d3.csv(base + 'recalls_clean.csv');
    const flagged = records.filter(r => r.do_not_drive === 'true' || r.park_outside === 'true');
    const years = d3.range(d3.min(flagged, r => +r.year), d3.max(flagged, r => +r.year) + 1);
    const max = d3.max(['do_not_drive', 'park_outside'], field => d3.max(Array.from(d3.rollup(flagged.filter(r => r[field] === 'true'), v => v.length, r => `${r.component_group}|${r.year}`).values())));
    function render() {
      container.replaceChildren();
      const park = select.value === 'park_outside';
      const color = d3.scaleSequential(d3.interpolateRgb(park ? '#fff2df' : '#fbece4', park ? '#aa5a0c' : '#a8352b')).domain([0, max]);
      container.classList.toggle('park-theme', park);
      const selected = flagged.filter(r => r[select.value] === 'true');
      const counts = d3.rollup(selected, v => v.length, r => r.component_group, r => +r.year);
      const groups = Array.from(counts, ([group, yearCounts]) => ({ group, total: d3.sum(yearCounts.values()) })).sort((a, b) => b.total - a.total);
      const readout = document.createElement('p'); readout.className = 'heat-readout'; readout.textContent = `${selected.length} campaigns · select a square for details`; container.append(readout);
      const scroll = document.createElement('div'); scroll.className = 'heat-scroll'; container.append(scroll);
      const grid = document.createElement('div'); grid.className = 'heat-grid advisory-grid'; grid.style.setProperty('--years', years.length); scroll.append(grid);
      const first = document.createElement('span'); first.className = 'heat-label'; first.textContent = 'Component · total'; grid.append(first);
      years.forEach(year => { const label = document.createElement('span'); label.className = 'heat-year'; label.textContent = year; grid.append(label); });
      groups.forEach(({ group, total }) => {
        const label = document.createElement('span'); label.className = 'heat-label'; label.textContent = `${group} · ${total}`; grid.append(label);
        years.forEach(year => {
          const count = counts.get(group).get(year) || 0;
          const cell = document.createElement('button'); cell.className = 'heat-cell'; cell.type = 'button'; cell.style.backgroundColor = color(count); cell.setAttribute('aria-label', `${group}, ${year}: ${count} campaigns`);
          cell.addEventListener('click', () => { readout.textContent = `${select.selectedOptions[0].textContent} · ${group} · ${year}: ${count} campaigns`; }); grid.append(cell);
        });
      });
      const legend = document.createElement('div'); legend.className = 'heat-legend'; legend.innerHTML = '<span>Fewer recalls</span><span class="heat-scale" aria-hidden="true"></span><span>More recalls</span>'; container.append(legend);
    }
    select.addEventListener('change', render); render();
  } catch { container.textContent = 'Unable to load advisory data. Run this page through a local web server and try again.'; }
}

async function showTrend() {
  try {
    const rows = await d3.csv(base + 'year_component_counts.csv', d => ({ year: +d.year, group: d.component_group, count: +d.recall_count }));
    const slider = document.querySelector('#start-year'), output = document.querySelector('#year-value'), play = document.querySelector('#play-years');
    const allMax = d3.max(rows, d => d.count);
    const names = Array.from(new Set(rows.map(d => d.group))).sort();
    const palette = ['#935323', '#386d9d', '#a83e3b', '#5b7d31', '#86559b', '#006f68', '#a76282', '#725b41', '#536b91', '#927315', '#b1495a', '#477a73', '#814e60', '#637c45', '#a45d25', '#5968a0', '#8c6334', '#30696f', '#906453', '#6d6493'];
    const colors = d3.scaleOrdinal(names, palette);
    const totals = d3.rollup(rows, values => d3.sum(values, d => d.count), d => d.group);
    const leaders = Array.from(totals, ([group, count]) => ({ group, count })).sort((a, b) => b.count - a.count).slice(0, 6).map(d => d.group);
    const years = d3.range(d3.min(rows, d => d.year), d3.max(rows, d => d.year) + 1);
    const lookup = d3.rollup(rows, values => values[0].count, d => d.group, d => d.year);
    const lineContainer = d3.select('#trend-lines');
    const width = 960, height = 300, x = d3.scaleLinear().domain(d3.extent(years)).range([55, width - 20]);
    const y = d3.scaleLinear().domain([0, d3.max(rows.filter(d => leaders.includes(d.group)), d => d.count)]).nice().range([height - 35, 15]);
    const svg = lineContainer.append('svg').attr('viewBox', `0 0 ${width} ${height}`).attr('role', 'img').attr('aria-label', 'Annual recall counts for the six most recalled component groups overall');
    const line = d3.line().x(d => x(d.year)).y(d => y(d.count));
    const paths = svg.selectAll('.trend-line').data(leaders).join('path').attr('class', 'trend-line').attr('fill', 'none').attr('stroke', group => colors(group)).attr('stroke-width', 2.5);
    const marker = svg.append('line').attr('y1', 15).attr('y2', height - 35).attr('stroke', '#666').attr('stroke-width', 1.5).attr('stroke-dasharray', '4 4');
    const hoverMarker = svg.append('line').attr('y1', 15).attr('y2', height - 35).attr('stroke', '#666').attr('stroke-width', 1).attr('stroke-dasharray', '3 3').attr('visibility', 'hidden').attr('pointer-events', 'none');
    const readout = lineContainer.append('div').attr('class', 'line-readout').attr('aria-live', 'polite');
    const hint = 'After playback, move over the graph to inspect a year. The year slider also shows these values.';
    readout.text(hint);
    svg.append('rect').attr('x', 55).attr('y', 15).attr('width', width - 75).attr('height', height - 50).attr('fill', 'transparent')
      .on('pointermove', function (event) {
        if (timer || +slider.value !== +slider.max) return;
        const year = Math.max(years[0], Math.min(years[years.length - 1], Math.round(x.invert(d3.pointer(event, svg.node())[0]))));
        hoverMarker.attr('x1', x(year)).attr('x2', x(year)).attr('visibility', 'visible');
        readout.selectAll('*').remove();
        readout.append('strong').text(year);
        const list = readout.append('div').attr('class', 'line-values');
        leaders.forEach(group => { const item = list.append('span'); item.append('i').style('background-color', colors(group)); item.append('span').text(`${group}: ${(lookup.get(group)?.get(year) || 0).toLocaleString()}`); });
      })
      .on('pointerleave', () => { hoverMarker.attr('visibility', 'hidden'); readout.text(hint); });
    const chart = d3.select(trend).append('div').attr('class', 'year-bubbles');
    let timer = null;
    function render() {
      const year = +slider.value; output.textContent = year;
      hoverMarker.attr('visibility', 'hidden'); readout.text(hint);
      marker.attr('x1', x(year)).attr('x2', x(year));
      paths.attr('d', group => line(years.filter(y => y <= year).map(y => ({ year: y, count: lookup.get(group)?.get(y) || 0 }))));
      const groups = leaders.map(group => ({ group, count: lookup.get(group)?.get(year) || 0 }));
      const items = chart.selectAll('.year-bubble').data(groups, d => d.group).join(enter => { const item = enter.append('div').attr('class', 'year-bubble'); item.append('strong'); item.append('span'); return item; }, update => update, exit => exit.remove()).order();
      items.style('--size', d => `${Math.round(55 + 200 * Math.sqrt(d.count / allMax))}px`).style('--bubble-color', d => colors(d.group)).attr('aria-label', d => `${d.group}: ${d.count} recall campaigns in ${year}`);
      items.select('strong').text(d => d.count.toLocaleString()); items.select('span').text(d => d.group);
    }
    slider.min = d3.min(rows, d => d.year); slider.max = d3.max(rows, d => d.year); slider.value = slider.min;
    slider.addEventListener('input', render); render();
    function stop() { clearInterval(timer); timer = null; play.textContent = 'Play timeline'; }
    play.addEventListener('click', () => {
      if (timer) { stop(); return; }
      if (+slider.value === +slider.max) slider.value = slider.min;
      render(); play.textContent = 'Pause timeline';
      timer = setInterval(() => { if (+slider.value >= +slider.max) { stop(); return; } slider.value = +slider.value + 1; render(); }, 900);
    });
  } catch (error) { trend.textContent = 'Unable to load the component data. Run this page through a local web server and check your connection.'; }
}

showTrend();
showAdvisoryExplorer();
