package web3.beaglegaze.spring_boot_sample;

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
