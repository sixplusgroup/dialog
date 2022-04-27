package emotion.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class StaffCardBaseInfo {
    private String staffName;
    @JsonProperty("CSSId")
    private Long CSSId;
    @JsonProperty("NumOfCase")
    private Integer NumOfCase;
    private Double serviceEvaluation;
}
