package emotion.controller;

import emotion.dto.CaseCardBaseInfo;
import emotion.service.CaseService;
import emotion.utils.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/case")
public class CaseController {
    @Autowired
    private CaseService caseService;

    @GetMapping("/get_typical_case_card_base_infos")
    public Response getTypicalCaseCardBaseInfos(){
        return caseService.getTypicalCaseCardBaseInfos();
    }

    @GetMapping("/get_loudness")
    public Response getDisplayedCaseLoudness(@RequestParam("caseName")String caseName, @RequestParam("staffId") Long staffId){
        return caseService.getDisplayedCaseLoudness(caseName,staffId);
    }

    @GetMapping("/get_case_dialogue_list")
    public Response getCaseDialogueList(@RequestParam("caseName")String caseName, @RequestParam("staffId") Long staffId){
        return caseService.getCaseDialogueList(caseName,staffId);
    }

    @GetMapping("/get_recommendation_point_list")
    public Response getRecommendationPointList(@RequestParam("caseName")String caseName, @RequestParam("staffId") Long staffId){
        return caseService.getRecommendationPointList(caseName,staffId);
    }

    @GetMapping("/get_case_evaluation")
    public Response getCaseEvaluationByCaseNameAndStaffId(@RequestParam("caseName")String caseName, @RequestParam("staffId")Long staffId){
        return caseService.getCaseEvaluationByCaseNameAndStaffId(caseName,staffId);
    }

    @GetMapping("/get_staff_case_card_base_infos")
    public Response getCaseCardBaseInfosByStaffId(@RequestParam("staffId") Long staffId){
        return caseService.getCaseCardBaseInfosByStaffId(staffId);
    }
}
