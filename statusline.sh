#!/bin/bash
# Claude Code status line: countdown to the fourth Thursday of November.
cat >/dev/null

days_until() {
  local year=$1 first_dow first_thu target now
  first_dow=$(date -j -f "%Y-%m-%d %H" "$year-11-01 12" +%u)
  first_thu=$(( 1 + (4 - first_dow + 7) % 7 ))
  target=$(date -j -f "%Y-%m-%d %H" "$year-11-$(( first_thu + 21 )) 12" +%s)
  now=$(date -j -f "%Y-%m-%d %H" "$(date +%Y-%m-%d) 12" +%s)
  echo $(( (target - now) / 86400 ))
}

days=$(days_until "$(date +%Y)")
if [ "$days" -lt -4 ]; then
  days=$(days_until "$(( $(date +%Y) + 1 ))")
fi

if [ "$days" -lt 0 ]; then
  msg="🥧 Leftovers season"
elif [ "$days" -eq 0 ]; then
  msg="🦃 Happy Thanksgiving!"
elif [ "$days" -eq 1 ]; then
  msg="🦃 1 day to Thanksgiving"
else
  msg="🦃 $days days to Thanksgiving"
fi

printf '\033[38;2;232;134;58m%s\033[0m\n' "$msg"
