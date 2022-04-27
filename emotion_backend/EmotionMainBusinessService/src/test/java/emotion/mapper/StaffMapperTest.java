package emotion.mapper;

import emotion.po.Staff;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@SpringBootTest
@Transactional
public class StaffMapperTest {
    @Autowired
    private StaffMapper staffMapper;

    @Test
    public void testInsert() throws Exception{
        Staff staff = new Staff();
        staff.setName("a");
        staffMapper.insert(staff);
        System.out.println(staff.getId());
    }

    @Test
    public void testGetAllStaffsAndDeleteById() throws Exception{
        List<Staff> staffs = staffMapper.getAllStaffs();
        int old_len = staffs.size();
        staffMapper.deleteById(staffs.get(0).getId());
        staffs = staffMapper.getAllStaffs();
        assert old_len-staffs.size() == 1;
    }
}
