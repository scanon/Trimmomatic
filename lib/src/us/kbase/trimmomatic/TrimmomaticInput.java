
package us.kbase.trimmomatic;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: TrimmomaticInput</p>
 * <pre>
 * using KBaseFile.PairedEndLibrary
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_ws",
    "output_ws",
    "input_paired_end_library",
    "output_paired_end_library",
    "output_unpaired_forward",
    "output_unpaired_reverse"
})
public class TrimmomaticInput {

    @JsonProperty("input_ws")
    private String inputWs;
    @JsonProperty("output_ws")
    private String outputWs;
    @JsonProperty("input_paired_end_library")
    private String inputPairedEndLibrary;
    @JsonProperty("output_paired_end_library")
    private String outputPairedEndLibrary;
    @JsonProperty("output_unpaired_forward")
    private String outputUnpairedForward;
    @JsonProperty("output_unpaired_reverse")
    private String outputUnpairedReverse;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_ws")
    public String getInputWs() {
        return inputWs;
    }

    @JsonProperty("input_ws")
    public void setInputWs(String inputWs) {
        this.inputWs = inputWs;
    }

    public TrimmomaticInput withInputWs(String inputWs) {
        this.inputWs = inputWs;
        return this;
    }

    @JsonProperty("output_ws")
    public String getOutputWs() {
        return outputWs;
    }

    @JsonProperty("output_ws")
    public void setOutputWs(String outputWs) {
        this.outputWs = outputWs;
    }

    public TrimmomaticInput withOutputWs(String outputWs) {
        this.outputWs = outputWs;
        return this;
    }

    @JsonProperty("input_paired_end_library")
    public String getInputPairedEndLibrary() {
        return inputPairedEndLibrary;
    }

    @JsonProperty("input_paired_end_library")
    public void setInputPairedEndLibrary(String inputPairedEndLibrary) {
        this.inputPairedEndLibrary = inputPairedEndLibrary;
    }

    public TrimmomaticInput withInputPairedEndLibrary(String inputPairedEndLibrary) {
        this.inputPairedEndLibrary = inputPairedEndLibrary;
        return this;
    }

    @JsonProperty("output_paired_end_library")
    public String getOutputPairedEndLibrary() {
        return outputPairedEndLibrary;
    }

    @JsonProperty("output_paired_end_library")
    public void setOutputPairedEndLibrary(String outputPairedEndLibrary) {
        this.outputPairedEndLibrary = outputPairedEndLibrary;
    }

    public TrimmomaticInput withOutputPairedEndLibrary(String outputPairedEndLibrary) {
        this.outputPairedEndLibrary = outputPairedEndLibrary;
        return this;
    }

    @JsonProperty("output_unpaired_forward")
    public String getOutputUnpairedForward() {
        return outputUnpairedForward;
    }

    @JsonProperty("output_unpaired_forward")
    public void setOutputUnpairedForward(String outputUnpairedForward) {
        this.outputUnpairedForward = outputUnpairedForward;
    }

    public TrimmomaticInput withOutputUnpairedForward(String outputUnpairedForward) {
        this.outputUnpairedForward = outputUnpairedForward;
        return this;
    }

    @JsonProperty("output_unpaired_reverse")
    public String getOutputUnpairedReverse() {
        return outputUnpairedReverse;
    }

    @JsonProperty("output_unpaired_reverse")
    public void setOutputUnpairedReverse(String outputUnpairedReverse) {
        this.outputUnpairedReverse = outputUnpairedReverse;
    }

    public TrimmomaticInput withOutputUnpairedReverse(String outputUnpairedReverse) {
        this.outputUnpairedReverse = outputUnpairedReverse;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((("TrimmomaticInput"+" [inputWs=")+ inputWs)+", outputWs=")+ outputWs)+", inputPairedEndLibrary=")+ inputPairedEndLibrary)+", outputPairedEndLibrary=")+ outputPairedEndLibrary)+", outputUnpairedForward=")+ outputUnpairedForward)+", outputUnpairedReverse=")+ outputUnpairedReverse)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
