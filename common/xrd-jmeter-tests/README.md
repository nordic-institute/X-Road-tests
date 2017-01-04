# xrd-jmeter-tests

This folder contains X-Road JMeter tests.

## Maven
[pom.xml](pom.xml) file can be used to execute JMeter tests with Maven.

Execute test with `mvn clean verify` optionally adding maven parameters `-D<param_name>=<param-value>` that override JMeter test configuration.

Example:

`mvn clean verify -Dhost=xtee10.ci.kit -DClientXRoadInstance=XTEE-CI-XM -DServiceXRoadInstance=XTEE-CI-XM`

The full list of parameters is:
- proto - protocol used. For example: `http`, `https`.
- host - ip or DNS name of security server or tested service. For example: `xtee6.ci.kit`
- port - port listening for connection. For example: `80`
- path - path to service. For example: `/` or `/xrd-mock`
- threads - amount of threads to use in the main test. For example: `10`
- duration - duration of the main test. For example: `60`
- rampup - rampup duration of the main test. For example: `10`
- wthreads - amount of threads to use for the warmup. For example: `10`
- wduration - duration of the warmup. For example: `10`
- wrampup - rampup duration of the warmup. For example: `2`
- ClientXRoadInstance - X-Road instance of client. For example: `XTEE-CI`
- ClientMemberClass - member class of client. For example: `COM`
- ClientMemberCode - member code of client. For example: `00000002`
- ClientSubsystemCode - subsystem code of client. For example: `MockSystem`
- ServiceXRoadInstance - X-Road instance of service. For example: `XTEE-CI`
- ServiceMemberClass - member class of service. For example: `COM`
- ServiceMemberCode - member code of service. For example: `00000002`
- ServiceSubsystemCode - subsystem code of service. For example: `MockSystem`

## Jenkins integration

- Create new Maven project
- Checkout project from git or manually add common/xrd-jmeter-tests folder to Jenkins workspace
- Under "Build" -> "Root POM" add `common/xrd-jmeter-tests/pom.xml`
- Under "Build" -> "Goals and options" add `clean verify -Dhost=xtee10.ci.kit -DClientXRoadInstance=XTEE-CI-XM -DServiceXRoadInstance=XTEE-CI-XM` (note that you might need to add more parameters)
- Add "Post-build Actions" -> "Archive the artifacts"
- Under "Post-build Actions" -> "Archive the artifacts" -> "Files to archive" add `common/xrd-jmeter-tests/target/**/*.html, common/xrd-jmeter-tests/target/**/*.json, common/xrd-jmeter-tests/target/**/*.txt, common/xrd-jmeter-tests/target/jmeter-errors.xml, common/xrd-jmeter-tests/target/**/*.html, common/xrd-jmeter-tests/target/**/*.jtl, common/xrd-jmeter-tests/target/**/*.png`
- Add "Post-build Actions" -> "Publish Performance test result report"
- Under "Post-build Actions" -> "Publish Performance test result report" -> "Performance report" add new "Jmeter" report and fill "Report files" with `common/xrd-jmeter-tests/**/*.jtl`
