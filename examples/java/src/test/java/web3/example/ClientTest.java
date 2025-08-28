package web3.example;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import web3.beaglegaze.AsyncBatchProcessor;
import web3.beaglegaze.BatchMode;
import web3.beaglegaze.ContractConsumer;
import web3.beaglegaze.MicroPaymentAspect;
import web3.beaglegaze.SmartContract;
import web3.beaglegaze.example.Main;

public class ClientTest {

    @BeforeAll
    public static void setup() throws Exception {
        AsyncBatchProcessor asyncBatchProcessor = new AsyncBatchProcessor(BatchMode.OFF);
        asyncBatchProcessor.addObserver(new ContractConsumer(
                new SmartContract("0x289B72CEeaB48832261626D62E3daA87Fd90B024", "http://localhost:8545",
                        "0xcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc", 1000)));
        MicroPaymentAspect.setProcessor(asyncBatchProcessor);
    }

    @Test
    public void testMain() throws Exception {
        for (int i = 0; i < 10; i++) {
            Main.main(new String[] {});
            System.out.println("Called main " + (i + 1) + " times");
            Thread.sleep(1000);    
        }
        
    }
}
