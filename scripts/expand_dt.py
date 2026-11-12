# Extra sections + FAQs appended to date/time tool pages.
D = {}

D['date-difference-calculator'] = ("""
<section><h2>Days in each month</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Month</th><th class="n">Days</th><th>Month</th><th class="n">Days</th></tr></thead><tbody>
<tr><td>January</td><td class="n">31</td><td>July</td><td class="n">31</td></tr><tr><td>February</td><td class="n">28 (29 in leap years)</td><td>August</td><td class="n">31</td></tr>
<tr><td>March</td><td class="n">31</td><td>September</td><td class="n">30</td></tr><tr><td>April</td><td class="n">30</td><td>October</td><td class="n">31</td></tr>
<tr><td>May</td><td class="n">31</td><td>November</td><td class="n">30</td></tr><tr><td>June</td><td class="n">30</td><td>December</td><td class="n">31</td></tr></tbody></table></div>
<p>A year has 365 days, or 366 in a leap year. Leap years are divisible by 4, except century years that are not divisible by 400: 2028 is a leap year, 2100 will not be. A year has 52 weeks and 1 day (2 in a leap year), which is why a date moves one weekday later each year.</p></section>
<section><h2>Working days in a year</h2><p>2026 and 2027 each have <strong>261 weekdays</strong> (Monday to Friday); 2028 has 260. Subtract public holidays to get working days: the US has 11 federal holidays, so a federal employee has about 250 working days a year; England and Wales have 8 bank holidays.</p>
<h3>Counting tips</h3><ul><li><strong>Elapsed versus inclusive.</strong> March 1 to March 10 is 9 days elapsed, but 10 days if you count both the first and last day (for example, a hotel stay is counted in nights, a festival in days).</li>
<li><strong>Notice periods and deadlines.</strong> Check whether the rule counts calendar days or business days and whether the day of notice itself counts.</li>
<li><strong>Age in days.</strong> Someone born 10,000 days ago is about 27 years and 4 months old.</li></ul></section>""",
[("How many weekdays are there in 2027?", "261 weekdays (Monday to Friday). Subtract public holidays to get working days."),
 ("How do I count days including the start and end date?", "Add 1 to the elapsed number of days. From March 1 to March 10 is 9 days elapsed, or 10 days counting both dates."),
 ("Is 2028 a leap year?", "Yes. 2028 is divisible by 4 and is not a century year, so February 2028 has 29 days.")])

D['days-since-calculator'] = ("""
<section><h2>Useful milestones</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th class="n">Days</th><th>Roughly equals</th><th>Common use</th></tr></thead><tbody>
<tr><td class="n">30</td><td>1 month</td><td>Free trials, return windows</td></tr><tr><td class="n">90</td><td>About 3 months</td><td>Probation periods, habit tracking</td></tr>
<tr><td class="n">100</td><td>14 weeks 2 days</td><td>100-day milestones, new jobs</td></tr><tr><td class="n">180</td><td>About 6 months</td><td>Visa and residency day counts</td></tr>
<tr><td class="n">365</td><td>1 year</td><td>Anniversaries, sobriety and streak milestones</td></tr><tr><td class="n">1,000</td><td>2 years 9 months</td><td>Relationship and baby milestones</td></tr>
<tr><td class="n">10,000</td><td>27 years 4 months</td><td>A "10,000 days old" celebration</td></tr></tbody></table></div></section>
<section><h2>Why the count can differ by one</h2><p>This calculator counts <strong>elapsed days</strong>: the start date is day 0, so yesterday is 1 day ago. Some trackers count the start date as day 1, which gives a number one higher. Habit and recovery apps often use the "day 1" convention, while contracts and official deadlines usually count elapsed days from the day after the event.</p>
<p>Because the count uses your device's calendar date at noon, daylight saving changes do not shift the result.</p></section>""",
[("How many days has it been since January 1?", "Enter January 1 of this year. The result is the number of full days elapsed; on January 2 it is 1."),
 ("How many days is 1,000 days?", "1,000 days is about 2 years and 9 months, or 142 weeks and 6 days."),
 ("Does the count include today?", "It counts elapsed days, so the start date is day zero. Add one if you want to count the start date as day one.")])

D['weeks-until-calculator'] = ("""
<section><h2>Weeks and days reference</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th class="n">Days</th><th class="n">Weeks</th><th class="n">Days</th><th class="n">Weeks</th></tr></thead><tbody>
<tr><td class="n">7</td><td class="n">1</td><td class="n">90</td><td class="n">12 weeks 6 days</td></tr><tr><td class="n">14</td><td class="n">2</td><td class="n">100</td><td class="n">14 weeks 2 days</td></tr>
<tr><td class="n">30</td><td class="n">4 weeks 2 days</td><td class="n">180</td><td class="n">25 weeks 5 days</td></tr><tr><td class="n">60</td><td class="n">8 weeks 4 days</td><td class="n">365</td><td class="n">52 weeks 1 day</td></tr></tbody></table></div>
<p>A month averages 4.35 weeks (365 ÷ 12 ÷ 7), so "about a month away" is roughly 4 to 4½ weeks.</p></section>
<section><h2>Planning with weeks</h2><ul>
<li><strong>Pregnancy</strong> is counted in weeks from the first day of the last menstrual period; a typical due date is 40 weeks (280 days) after it.</li>
<li><strong>Training plans</strong> for a half-marathon are usually 10 to 12 weeks, and for a marathon 16 to 20 weeks.</li>
<li><strong>Notice and delivery times</strong> quoted in weeks normally mean calendar weeks, including weekends.</li>
<li><strong>Weekly budgets:</strong> divide an amount by the weeks remaining to see how much to set aside each week; $1,200 over 16 weeks is $75 a week.</li></ul></section>""",
[("How many weeks are in a year?", "52 weeks and 1 day, or 52 weeks and 2 days in a leap year."),
 ("How many weeks are in a month?", "About 4.35 weeks on average. February has exactly 4 weeks in a non-leap year."),
 ("How do I convert days to weeks?", "Divide by 7. The whole number is full weeks and the remainder is extra days: 100 days is 14 weeks and 2 days.")])

D['birthday-countdown'] = ("""
<section><h2>Birthday facts the calculator handles</h2><ul>
<li><strong>February 29 birthdays:</strong> in years without February 29, most people celebrate on February 28 or March 1. Legally, many countries treat March 1 as the birthday in non-leap years for age-based rules.</li>
<li><strong>Day of the week:</strong> your birthday moves forward one weekday each year, or two after February 29 of a leap year.</li>
<li><strong>Time zones:</strong> the countdown uses your device's local date, so someone travelling may see the day change at a different moment.</li></ul></section>
<section><h2>Age milestones</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Milestone</th><th>Approximate age</th></tr></thead><tbody>
<tr><td>1,000 days old</td><td>2 years 9 months</td></tr><tr><td>10,000 days old</td><td>27 years 4 months</td></tr><tr><td>20,000 days old</td><td>54 years 9 months</td></tr>
<tr><td>1 billion seconds old</td><td>31 years 8 months</td></tr><tr><td>Half-birthday</td><td>Six months after the birthday</td></tr></tbody></table></div>
<p>Planning a party? Most people send invitations 3 to 4 weeks ahead, and venues for popular dates are often booked 2 to 3 months in advance.</p></section>""",
[("What if my birthday is February 29?", "In non-leap years the countdown targets February 28 or March 1 depending on the calendar convention you use; check the result date it shows."),
 ("When will I be 10,000 days old?", "About 27 years and 4 months after you were born. The date difference calculator can find the exact day."),
 ("Does the countdown include today?", "It counts the days remaining until the birthday date; on the birthday itself the result is zero.")])

D['countdown-timer'] = ("""
<section><h2>Popular timer lengths</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Use</th><th>Time</th></tr></thead><tbody>
<tr><td>Pomodoro focus block</td><td>25 minutes, then a 5-minute break; a longer 15–30 minute break after four blocks</td></tr>
<tr><td>Soft-boiled / hard-boiled egg</td><td>6–7 minutes / 10–12 minutes after the water boils</td></tr>
<tr><td>Plank or interval set</td><td>30–60 seconds</td></tr><tr><td>Tea steeping</td><td>3–5 minutes for black tea, 2–3 for green</td></tr>
<tr><td>Presentation or speech practice</td><td>5, 10 or 20 minutes</td></tr><tr><td>Brushing teeth</td><td>2 minutes</td></tr></tbody></table></div></section>
<section><h2>Tips for reliable timing</h2><ul>
<li>Keep this tab open. Browsers may slow timers in background tabs to save battery, so the display can lag; the remaining time is recalculated when you return.</li>
<li>Check your device volume if you rely on the alert.</li>
<li>For deadlines on a calendar date rather than a duration, use the weeks-until or date difference calculator.</li></ul></section>""",
[("How does the Pomodoro technique work?", "Work for 25 minutes, take a 5-minute break, and after four work blocks take a longer break of 15 to 30 minutes."),
 ("Will the timer keep running if I switch tabs?", "Yes, but some browsers slow background timers. Keep the tab visible for the most accurate countdown."),
 ("Can I set a timer longer than an hour?", "Yes. Enter the total minutes, for example 90 minutes for an hour and a half.")])

D['stopwatch'] = ("""
<section><h2>Lap times and splits</h2><p>A <strong>lap</strong> records the time since the previous lap; a <strong>split</strong> is the total time since the start. If you press Lap at 1:05 and again at 2:15, the second lap took 1:10 and the split is 2:15. Comparing laps shows whether you are speeding up or slowing down.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Activity</th><th>What to time</th></tr></thead><tbody>
<tr><td>Running</td><td>Each lap of a 400 m track or each kilometre</td></tr><tr><td>Meetings</td><td>Each agenda item, to see where time goes</td></tr>
<tr><td>Work tasks</td><td>Real time per task, to estimate future jobs and bill accurately</td></tr><tr><td>Cooking</td><td>Steps that need precise timing</td></tr></tbody></table></div></section>
<section><h2>From stopwatch time to timesheet</h2><p>Timesheets and payroll usually need decimal hours. Divide minutes by 60: 1 hour 45 minutes is <strong>1.75 hours</strong>, and 2 hours 20 minutes is <strong>2.33 hours</strong>. The decimal hours converter does this for you, and the time card calculator adds up a full week.</p></section>""",
[("What is the difference between a lap and a split?", "A lap is the time since the previous lap; a split is the total time since the stopwatch started."),
 ("How do I convert stopwatch time to decimal hours?", "Divide the minutes by 60 and add them to the hours. 1 hour 45 minutes is 1.75 hours."),
 ("Is the online stopwatch accurate?", "It uses the browser's high-resolution clock and is accurate to a fraction of a second for everyday timing. It is not certified for official sports timing.")])

D['time-add-subtract'] = ("""
<section><h2>Adding times by hand</h2><ol><li>Add the hours and the minutes separately: 2 h 45 m + 1 h 30 m = 3 h 75 m.</li>
<li>Convert every 60 minutes into an hour: 75 minutes = 1 h 15 m.</li><li>Total: <strong>4 hours 15 minutes</strong>.</li></ol>
<p>To subtract, borrow 60 minutes from the hours when needed: 5 h 10 m − 2 h 40 m becomes 4 h 70 m − 2 h 40 m = <strong>2 h 30 m</strong>.</p></section>
<section><h2>Minutes to decimal hours</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Minutes</th><th class="n">Decimal</th><th>Minutes</th><th class="n">Decimal</th></tr></thead><tbody>
<tr><td>5</td><td class="n">0.08</td><td>35</td><td class="n">0.58</td></tr><tr><td>10</td><td class="n">0.17</td><td>40</td><td class="n">0.67</td></tr>
<tr><td>15</td><td class="n">0.25</td><td>45</td><td class="n">0.75</td></tr><tr><td>20</td><td class="n">0.33</td><td>50</td><td class="n">0.83</td></tr>
<tr><td>25</td><td class="n">0.42</td><td>55</td><td class="n">0.92</td></tr><tr><td>30</td><td class="n">0.50</td><td>60</td><td class="n">1.00</td></tr></tbody></table></div>
<p>The most common payroll mistake is writing 7 hours 30 minutes as 7.30 instead of <strong>7.5</strong>. At $20 an hour that underpays by $4 for that one entry.</p></section>""",
[("How do I add hours and minutes?", "Add hours and minutes separately, then convert each 60 minutes into one hour. 2 h 45 m + 1 h 30 m = 4 h 15 m."),
 ("How do I write 1 hour 30 minutes in decimal?", "1.5 hours. Divide the minutes by 60: 30 ÷ 60 = 0.5."),
 ("How do I subtract time?", "Subtract minutes from minutes and hours from hours, borrowing 60 minutes from the hours when the minutes would go negative.")])

D['time-duration-calculator'] = ("""
<section><h2>Common shift lengths</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Start</th><th>End</th><th class="n">Duration</th><th class="n">With 30-min unpaid break</th></tr></thead><tbody>
<tr><td>9:00 AM</td><td>5:00 PM</td><td class="n">8 h</td><td class="n">7.5 h</td></tr><tr><td>8:30 AM</td><td>5:00 PM</td><td class="n">8 h 30 m</td><td class="n">8 h</td></tr>
<tr><td>7:00 AM</td><td>3:30 PM</td><td class="n">8 h 30 m</td><td class="n">8 h</td></tr><tr><td>7:00 PM</td><td>7:00 AM</td><td class="n">12 h</td><td class="n">11.5 h</td></tr>
<tr><td>11:00 PM</td><td>7:00 AM</td><td class="n">8 h</td><td class="n">7.5 h</td></tr></tbody></table></div></section>
<section><h2>24-hour clock quick guide</h2><p>Afternoon times add 12 to the hour: 1:00 PM is 13:00 and 6:45 PM is 18:45. Midnight is 00:00 and noon is 12:00. Working in 24-hour time avoids AM/PM mistakes: 21:30 − 14:15 = 7 h 15 m.</p>
<p><strong>Daylight saving time:</strong> an overnight shift on the night the clocks change is one hour shorter (spring) or longer (autumn) in real time than the clock times suggest. Employers must pay for the hours actually worked.</p></section>""",
[("How do I calculate hours between two times?", "Convert both times to minutes from midnight, subtract the start from the end, and add 24 hours if the end time is earlier (the period crossed midnight)."),
 ("How long is a 7 PM to 7 AM shift?", "12 hours, or 11.5 paid hours with a 30-minute unpaid break."),
 ("How do daylight saving changes affect a night shift?", "On the spring change a night shift is one hour shorter in real time, and on the autumn change one hour longer. Pay should follow the actual hours worked.")])

D['time-from-now-calculator'] = ("""
<section><h2>Quick reference</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Period</th><th class="n">In hours</th><th class="n">In minutes</th></tr></thead><tbody>
<tr><td>1 day</td><td class="n">24</td><td class="n">1,440</td></tr><tr><td>1 week</td><td class="n">168</td><td class="n">10,080</td></tr>
<tr><td>30 days</td><td class="n">720</td><td class="n">43,200</td></tr><tr><td>1 year</td><td class="n">8,760</td><td class="n">525,600</td></tr></tbody></table></div></section>
<section><h2>Everyday uses</h2><ul>
<li><strong>Medication schedules:</strong> a dose every 8 hours starting at 7:00 AM falls at 3:00 PM and 11:00 PM. Follow the label or your pharmacist's instructions.</li>
<li><strong>Parking and rentals:</strong> a 72-hour parking limit starting Friday 6:00 PM ends Monday 6:00 PM.</li>
<li><strong>Shipping and response times:</strong> "within 48 hours" from Wednesday noon is Friday noon.</li>
<li><strong>Time zones:</strong> the result uses your device's time zone. For another city, convert with the time zone converter.</li></ul>
<p>Around a daylight saving change, adding "24 hours" and adding "1 day" can give different clock times; this calculator adds exact elapsed time.</p></section>""",
[("What time will it be in 72 hours?", "The same clock time three days later, unless a daylight saving change happens in between."),
 ("How many hours are in a week?", "168 hours (7 × 24)."),
 ("Does the calculator use my time zone?", "Yes. It uses the time and time zone set on your device.")])

D['sleep-calculator'] = ("""
<section><h2>How much sleep do you need?</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Age</th><th>Recommended sleep per day</th></tr></thead><tbody>
<tr><td>Teenagers (13–18)</td><td>8–10 hours</td></tr><tr><td>Adults (18–60)</td><td>7 or more hours</td></tr><tr><td>Adults 61–64</td><td>7–9 hours</td></tr><tr><td>65 and older</td><td>7–8 hours</td></tr></tbody></table></div>
<p class="tp-note">Based on recommendations published by the US Centers for Disease Control and Prevention. Individual needs vary.</p></section>
<section><h2>About 90-minute cycles</h2><p>Sleep moves through light, deep and REM stages in cycles that average about 90 minutes, though real cycles range from roughly 70 to 120 minutes and change through the night. Waking at the end of a cycle, during light sleep, can feel easier than waking from deep sleep. Treat the times as a starting point and adjust by 15 minutes either way to see what works for you.</p>
<h3>Habits that help</h3><ul><li>Keep the same wake-up time every day, including weekends.</li><li>Avoid caffeine in the 6 hours before bed.</li><li>Keep the bedroom dark, quiet and cool.</li><li>If you regularly feel unrested after enough sleep, talk to a doctor.</li></ul></section>""",
[("What time should I go to bed to wake up at 6 AM?", "For five 90-minute cycles plus about 15 minutes to fall asleep, around 10:15 PM; for six cycles, around 8:45 PM."),
 ("How long is a sleep cycle?", "About 90 minutes on average, though cycles vary from roughly 70 to 120 minutes."),
 ("How many hours of sleep do adults need?", "At least 7 hours a night for most adults, according to the CDC.")])

D['time-budget-calculator'] = ("""
<section><h2>How Americans spend a day</h2><p>The US Bureau of Labor Statistics American Time Use Survey finds that people aged 15 and over spend roughly 9 hours a day sleeping, around 5 hours on leisure and sports (about half of it watching TV), and about 3½ hours working when averaged across all days and people, including those who do not work. Employed people work about 7½ to 8 hours on the days they work.</p></section>
<section><h2>Your year in hours</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Daily habit</th><th class="n">Hours a week</th><th class="n">Hours a year</th><th class="n">Full days a year</th></tr></thead><tbody>
<tr><td>30 minutes</td><td class="n">3.5</td><td class="n">183</td><td class="n">7.6</td></tr><tr><td>1 hour</td><td class="n">7</td><td class="n">365</td><td class="n">15.2</td></tr>
<tr><td>2 hours</td><td class="n">14</td><td class="n">730</td><td class="n">30.4</td></tr><tr><td>3 hours</td><td class="n">21</td><td class="n">1,095</td><td class="n">45.6</td></tr></tbody></table></div>
<p>A daily one-hour commute adds up to 365 hours a year, about 9 working weeks. Cutting 30 minutes of daily screen time frees about 183 hours, enough for a short course or roughly 30 books.</p></section>""",
[("How many hours a year is one hour a day?", "365 hours, or about 15 full days."),
 ("How many free hours does a typical full-time worker have?", "With 8 hours of sleep, 8 of work and 1 of commuting, about 7 hours remain for chores, meals, family and leisure on a workday."),
 ("Where does the average person's time go?", "According to the American Time Use Survey, the largest blocks are sleep, work and leisure, with TV taking about half of leisure time.")])
