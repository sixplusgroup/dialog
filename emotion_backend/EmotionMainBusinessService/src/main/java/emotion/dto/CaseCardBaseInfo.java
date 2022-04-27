package emotion.dto;

import lombok.Data;

import java.util.Set;

@Data
public class CaseCardBaseInfo {
    private String caseName;
    private String typicalPoint;
    private String staffName;
    private String date;
    private Long staffId;
    private Set<String> emotions;
}
