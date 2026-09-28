/**
 * JoRoScope: calendar export. Builds iCalendar (.ics, RFC 5545) files that phone and desktop
 * calendars import: timed events in UTC, all-day events as dates, text escaped and long lines
 * folded at 75 bytes. Loaded before app.js; also required by the Node tests.
 */
function icsEscape(text) {
  return String(text ?? '').replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
}

// Fold a content line into 75-byte pieces without splitting a UTF-8 character (Tamil text is multi-byte)
function icsFold(line) {
  const bytes = s => new TextEncoder().encode(s).length;
  const out = [];
  let current = '';
  for (const ch of line) {
    const limit = out.length ? 74 : 75;  // continuation lines start with a space
    if (bytes(current + ch) > limit) {
      out.push(current);
      current = ch;
    } else {
      current += ch;
    }
  }
  out.push(current);
  return out.map((part, i) => (i ? ' ' + part : part)).join('\r\n');
}

const icsUtc = iso => new Date(iso).toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
const icsDate = ymd => ymd.replace(/-/g, '');
const icsNextDay = ymd => {
  const d = new Date(`${ymd}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + 1);
  return d.toISOString().slice(0, 10);
};

/**
 * events: [{uid, title, description, start, end}] where start/end are ISO date-times with an
 * offset for timed events, or 'YYYY-MM-DD' for an all-day event (end optional, inclusive).
 */
function buildIcs(events, calendarName, now = new Date()) {
  const stamp = icsUtc(now.toISOString());
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//JoRoScope//Vedic Astrology//EN', 'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH', `X-WR-CALNAME:${icsEscape(calendarName)}`];
  events.forEach(ev => {
    const allDay = /^\d{4}-\d{2}-\d{2}$/.test(ev.start);
    lines.push('BEGIN:VEVENT', `UID:${ev.uid}@joroscope.local`, `DTSTAMP:${stamp}`);
    if (allDay) {
      lines.push(`DTSTART;VALUE=DATE:${icsDate(ev.start)}`, `DTEND;VALUE=DATE:${icsDate(icsNextDay(ev.end || ev.start))}`,
        'TRANSP:TRANSPARENT');
    } else {
      lines.push(`DTSTART:${icsUtc(ev.start)}`, `DTEND:${icsUtc(ev.end || ev.start)}`);
    }
    lines.push(`SUMMARY:${icsEscape(ev.title)}`);
    if (ev.description) lines.push(`DESCRIPTION:${icsEscape(ev.description)}`);
    lines.push('END:VEVENT');
  });
  lines.push('END:VCALENDAR');
  return lines.map(icsFold).join('\r\n') + '\r\n';
}

// Hand a text file to the browser's download
function downloadText(filename, text, type) {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
}

if (typeof module !== 'undefined') module.exports = { buildIcs, icsFold, icsEscape };
