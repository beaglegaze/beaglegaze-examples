# Beaglegaze Spring Boot Sample
Welcome to the Spring Boot Sample. This sample repository shows how to use the [beaglegaze-java-sdk](https://github.com/beaglegaze/beaglegaze-java-sdk) to monetize your Spring Boot App.

## Setup

### Dependency Management
Add the following dependencies to your `pom.xml`:
```xml
<dependency>
    <groupId>web3.beaglegaze</groupId>
    <artifactId>beaglegaze-java-sdk</artifactId>
    <version>v0.0.10</version>
</dependency>
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjrt</artifactId>
    <version>1.9.7</version>
</dependency>
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjweaver</artifactId>
    <version>1.9.7</version>
</dependency>
```

Additionally, add the following build plugins to your `pom.xml`:
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>aspectj-maven-plugin</artifactId>
            <version>1.15.0</version>
            <configuration>
                <complianceLevel>16</complianceLevel>
                <source>16</source>
                <target>16</target>
                <showWeaveInfo>true</showWeaveInfo>
                <verbose>true</verbose>
                <weaveDependencies>
                    <weaveDependency>
                        <groupId>web3.beaglegaze</groupId>
                        <artifactId>beaglegaze-java-sdk</artifactId>
                    </weaveDependency>
                </weaveDependencies>
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>compile</goal>
                        <goal>test-compile</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### Beaglegaze Config
In the class `src/main/java/web3/beaglegaze/spring-boot-sample/BeaglegazeConfig` you see how to initialize the `Beaglegaze Payment Processor`:
```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import jakarta.annotation.PostConstruct;
import web3.beaglegaze.AsyncBatchProcessor;
import web3.beaglegaze.BatchMode;
import web3.beaglegaze.ContractConsumer;
import web3.beaglegaze.MicroPaymentAspect;
import web3.beaglegaze.SmartContract;

@Configuration
public class BeaglegazeConfig {


    @Value("${beaglegaze.account.private-key}")
    private String accountPrivateKey;

    @PostConstruct
    public void init() throws Exception {
        AsyncBatchProcessor asyncBatchProcessor = new AsyncBatchProcessor(BatchMode.OFF);
        asyncBatchProcessor.addObserver(new ContractConsumer(
                new SmartContract("0x289B72CEeaB48832261626D62E3daA87Fd90B024", "http://localhost:8545",
                        accountPrivateKey, 1000)));
        MicroPaymentAspect.setProcessor(asyncBatchProcessor);
    }

}
```
### The Endpoint
Finally, add the `PayPerCall`-Annotation to your REST-Endpoint(s):

```java
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import web3.beaglegaze.PayPerCall;

@RestController
public class SampleRestController {
    

    /**
     * This endpoint is pay-per-call enabled.
     */
    @GetMapping("/hello")
    @PayPerCall(price = 100)
    public String hello() {
        return "Hello, World!";
    }

}
```

### Building
Now, build the application:

```bash
mvn verify
```
Before running the application, make sure your IDE did not rebuild it; earlier, we configured our Maven Build in a way to weave the `PayPerCall` aspect into your code; your IDE won't do this when building your app. 

### Pre-Executing
Before running your app, spin up a local ethereum node. You can use the Beaglegaze Hardhat Testnet; there you will have the Beaglegaze Smart Contract already deployed at the address configured in this sample.

```bash
git clone git@github.com:beaglegaze/beaglegaze-web3.git
cd beaglegaze-web3/eth-dev-node/
docker build -t hardhat-testnet .
docker run -it -p 8545:8545 hardhat-testnet
```
The private key configured in the `src/main/resources/application.properties` belongs to a prefunded account in the `hardhat-testnet`. Make sure to not use it in production in any way!

### Starting the Server
Now you are ready to start the server:

```bash
mvn spring-boot:run
```
And finally, curl the `/hello` endpoint:

```bash
curl http://localhost:8080/hello
```

The first call will succeed, despite the fact that there is no funding yet:

```
Hello, World!
```

This is due to the async nature of the beaglegaze-java-sdk. The second (and every other call) will then fail:

```
{"timestamp":"2025-10-21T19:11:38.664+00:00","status":500,"error":"Internal Server Error","path":"/hello"}
```

Checking the server logs, you will notice a stacktrace coming from beaglegaze:

```
java.lang.RuntimeException: Micro-payment processing is in error state, method execution blocked.
        at web3.beaglegaze.spring_boot_sample.SampleRestController.hello_aroundBody1$advice(SampleRestController.java:24) ~[classes/:na]
[...]
```

Beaglegaze successfully checked the client's missing account balance and intercepted the code execution!
Next, let's use the Beaglegaze Web Dashboard to fund our account, unlocking beaglegaze again.

### Fund the Beaglegaze Contract
Use the Beaglegaze Web Dashboard to fund the client account. For the next steps, you need a browser with MetaMask installed.

```bash
git clone git@github.com:beaglegaze/beaglegaze-web.git
cd beaglegaze-web/
npm run dev
```

In your browser, connect Metamask to `localhost:8454` and import the wallet by providing the private key: `0xcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc`.

You should see a wallet with 1000 ETH in it.

Open `http://localhost:3000` and connect your wallet.

In the Web UI, add the `Beaglegaze` Contract by it's address `0x289B72CEeaB48832261626D62E3daA87Fd90B024`.

Alternatively, you can just send 2 ETH to the contract address. Make sure to use the same wallet which private key is configured in your `application.properties`.

After funding, you should be able to call the `/hello` endpoint again.

Congratulations, you successfully "payed" for using a piece of open-source software.