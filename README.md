# Assignment-no.1 Design and implement an automated testing framework for a "User Management API", including test cases for core interfaces, execution scripts, and report generation. 
#TEST DESIGN
Positive tests: happy path create → get → update → delete.

Negative tests: missing required fields, duplicate creation, invalid IDs, unauthorized access.

Edge cases: extremely long strings, invalid email format, invalid JSON, concurrency tests (race conditions).

Data isolation: tests should create and clean up their own resources. Use a separate test tenant or DB if possible.

Idempotence: be cautious: delete tests should tolerate multiple delete attempts (200/204/404).

Assertions: check status code, response schema, critical fields, and side effects.

Contract tests: consider adding JSON Schema validation for responses.
