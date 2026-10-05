---
title: "ICU Patient Telemetry Watchdog Supervisor"
type: app_lab
module: threads
unit: unit_1_2_thread_management
lab_number: 1
difficulty: easy
use_case: icu_telemetry_watchdog
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - threads
    - concurrency
  subtopics:
    - daemon-threads
    - thread-enumeration
    - cooperative-cancellation
    - liveness-checks
---

# Lab Level 1: ICU Patient Telemetry Watchdog Supervisor
**Module**: Threads
**Objective**: Build a background watchdog supervisor that monitors patient telemetry worker threads and orchestrates cooperative shutdown.
**Difficulty**: Easy
**Context**: Healthcare Patient Monitoring

## Generic Information
**Problem Statement**: In a hospital intensive care unit, background worker threads continuously read patient vital telemetry. If a telemetry thread crashes or becomes unresponsive, hospital nurses must be immediately alerted. Furthermore, when shutting down or restarting the gateway, all active telemetry workers must be signaled to gracefully close device connections without stranding sockets.
**Goals**:
- Run a background watchdog supervisor thread as a daemon.
- Detect dead or unresponsive telemetry threads using `threading.enumerate()` and `is_alive()`.
- Implement graceful cooperative shutdown across all monitored worker threads using `threading.Event`.
**Data Elements**:
- `patient_id` (str): Unique patient identifier (e.g. "PAT-301").
- `thread_name` (str): Structured thread name formatted as `f"Telemetry-{patient_id}"`.
- `health_status` (dict): Dictionary mapping `patient_id` to liveness boolean.

## Use Case
**Title**: Monitor and Coordinate Patient Telemetry Threads
**Description**: The supervisor discovers all active telemetry workers by prefix, tracks their liveness status, and provides an orderly shutdown mechanism.

### Rules
- Telemetry worker threads must respond cooperatively to a shared `threading.Event`.
- The watchdog scan must inspect active threads using `threading.enumerate()`.
- Shutdown must signal all workers and wait with a timeout.

### Test Cases
- Case 1: Detect all registered telemetry workers as active.
- Case 2: Detect when a worker thread terminates and flag its liveness as `False`.
- Case 3: Trigger shutdown event and verify all workers terminate cleanly within timeout.

### Success Criteria
- Watchdog accurately identifies which patient telemetry threads are alive.
- Shutdown cleanly joins all threads within 1 second.
- No dangling non-daemon threads prevent process termination.

## Overview
This lab guides you through building `ICUWatchdogSupervisor`, an enterprise reliability component that tracks worker threads in real time and handles graceful application termination.

## Learning Goals
- Use `threading.enumerate()` to discover threads matching a prefix.
- Use `threading.Event` to broadcast shutdown signals.
- Safely join worker threads using timeouts.

## How to Use This Lab
1. Read `README.md` and `tasks.md`.
2. Implement methods in `starter_code.py`.
3. Run `python tests.py` to verify implementation.
4. Review `solution/solution.py` after completion.

## Task Summary
- Task 1: Implement `TelemetryWorker` class inheriting from `threading.Thread` with cooperative loop.
- Task 2: Implement `ICUWatchdogSupervisor.get_active_telemetry_patients()`.
- Task 3: Implement `ICUWatchdogSupervisor.shutdown_all(timeout)`.
