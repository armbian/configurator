#!/usr/bin/env bats

@test "Test" {
  configurator
  [ "$status" -eq 1 ]
  [ "$output" == '' ]
}
