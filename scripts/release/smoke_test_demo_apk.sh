#!/usr/bin/env bash
set -euo pipefail

ANDROID_PACKAGE_NAME="org.midistream.midistreamdemo"
PASS_MARKER="MIDISTREAM_DEMO_PASS"
FAIL_MARKER="MIDISTREAM_DEMO_FAIL"

: "${EXPECTED_MIDISTREAM_VERSION:?}"

adb uninstall "$ANDROID_PACKAGE_NAME" >/dev/null 2>&1 || true
adb install -r -t demo.apk

adb shell getprop ro.product.cpu.abi
adb shell getprop ro.build.version.sdk
adb shell pm path "$ANDROID_PACKAGE_NAME"

adb logcat -c

echo "Launching $ANDROID_PACKAGE_NAME"
adb shell monkey -p "$ANDROID_PACKAGE_NAME" -c android.intent.category.LAUNCHER 1

required_markers=(
  "MIDISTREAM_APP_BUILD"
  "$PASS_MARKER"
  "MIDISTREAM_DEMO_START"
  "MIDISTREAM_VERSION=$EXPECTED_MIDISTREAM_VERSION"
  "MIDISTREAM_TEST_INIT=PASS"
  "MIDISTREAM_TEST_CONFIG=PASS"
  "MIDISTREAM_TEST_VOLUME=PASS"
  "MIDISTREAM_TEST_REVERB=PASS"
  "MIDISTREAM_TEST_WRITE=PASS"
)

echo "Waiting for smoke-test marker..."
deadline=$((SECONDS + 120))

while (( SECONDS < deadline )); do
  adb logcat -d > logcat.txt

  if grep -Fq "$FAIL_MARKER" logcat.txt; then
    echo "::error::Demo emitted failure marker"
    grep -E "MIDISTREAM_|midistream-demo" logcat.txt || true
    exit 1
  fi

  if grep -Fq "$PASS_MARKER" logcat.txt; then
    echo "Demo smoke test passed"
    break
  fi

  sleep 2
done

if ! grep -Fq "$PASS_MARKER" logcat.txt; then
  echo "::error::Timed out waiting for pass marker: $PASS_MARKER"
  grep -E "MIDISTREAM_|midistream-demo" logcat.txt || true
  exit 1
fi

missing=0

for marker in "${required_markers[@]}"; do
  if ! grep -Fq "$marker" logcat.txt; then
    echo "::error::Missing expected log marker: $marker"
    missing=1
  fi
done

echo "Observed Midistream markers:"
grep -E "MIDISTREAM_|midistream-demo" logcat.txt || true

if (( missing )); then
  exit 1
fi
