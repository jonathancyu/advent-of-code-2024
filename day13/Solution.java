import com.dashoptimization.ColumnType;
import com.dashoptimization.XPRSenumerations;
import com.dashoptimization.objects.XpressProblem;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;


public class Solution {
    @NoArgsConstructor
    @Setter
    private static class Problem {
        public long[] a;
        public long[] b;
        public long[] target;
        public long solve() {
            System.out.printf("a: %s, b: %s, t: %s%n", Arrays.toString(a), Arrays.toString(b), Arrays.toString(target));
            // Solve problem, add to total
            try (var problem = new XpressProblem()) {
                var aCount = problem.addVariable(ColumnType.Integer, "A");
                var bCount = problem.addVariable(ColumnType.Integer, "B");
                // X
                problem.addConstraint(aCount.mul(a[0]).plus(bCount.mul(b[0])).eq(target[0]));
                // Y
                problem.addConstraint(aCount.mul(a[1]).plus(bCount.mul(b[1])).eq(target[1]));
                // Minimize
                problem.chgObjSense(XPRSenumerations.ObjSense.MINIMIZE);
                problem.mipOptimize();
                var solStatus = problem.attributes().getSolStatus();
                if (Objects.equals(solStatus, XPRSenumerations.SolStatus.OPTIMAL)) {
                    // result
                    var a = Math.round(aCount.getSolution());
                    var b = Math.round(bCount.getSolution());
                    return 3L * a + b;
                } else {
                    System.out.printf("Skipped with soln: %s%n", solStatus);
                }
            }
            return 0;
        }
    }
    @Test
    public void adventOfCodeDay13() throws IOException {
        List<String> lines = Files.readAllLines(Path.of("src/test/resources/test.txt"));


        Problem problem = new Problem();
        long total = 0;
        for (String line : lines) {
            if (line.isBlank() && problem.target != null) {
                total += problem.solve();
                System.out.println(problem);
                problem = new Problem();
                continue;
            }
            var split = line.split(":")[1].strip().split("[,\\s]+");
            if (line.contains("Button A")) {
                var x = Long.parseLong(split[0].split("\\+")[1]);
                var y = Long.parseLong(split[1].split("\\+")[1]);
                problem.setA(new long[]{x, y});
            }else if (line.contains("Button B")) {
                var x = Long.parseLong(split[0].split("\\+")[1]);
                var y = Long.parseLong(split[1].split("\\+")[1]);
                problem.setB(new long[]{x, y});
            } else if (line.contains("Prize:")) {
                var x = 10000000000000L + Long.parseLong(split[0].split("=")[1]);
                var y = 10000000000000L + Long.parseLong(split[1].split("=")[1]);
                problem.setTarget(new long[]{x, y});
            }
        }
        if (problem.target != null) {
            total += problem.solve();
        }

        System.out.println(total);
    }
}
