-- Insert initial stu_info data
INSERT INTO stu_info (stu_id, name, class, clno, gender, dob, gmail, house)
VALUES (20201033, 'Fung Ching', '5D', 6, 'M', '2008-05-31', 's20201033@caremelss.edu.hk', 'Virtue');

-- Insert event data
INSERT INTO event (event_id, grade, gender, item, category) VALUES
(1, 'C', 'boys', '100m', 'racing'),
(2, 'C', 'boys', '200m', 'racing'),
(3, 'C', 'boys', '400m', 'racing'),
(4, 'C', 'boys', '60m', 'racing'),
(5, 'C', 'boys', '800m', 'racing'),
(6, 'C', 'boys', '1500m', 'racing'),
(7, 'C', 'boys', 'High Jump', 'field'),
(8, 'C', 'boys', 'Long Jump', 'field'),
(9, 'C', 'boys', 'Shot Put', 'field'),
(10, 'C', 'boys', 'Softball', 'field'),
(11, 'C', 'boys', '4x100', 'relay'),
(12, 'C', 'boys', '4x400', 'relay'),
(13, 'C', 'girls', '100m', 'racing'),
(14, 'C', 'girls', '200m', 'racing'),
(15, 'C', 'girls', '400m', 'racing'),
(16, 'C', 'girls', '60m', 'racing'),
(17, 'C', 'girls', '800m', 'racing'),
(18, 'C', 'girls', '1500m', 'racing'),
(19, 'C', 'girls', 'High Jump', 'field'),
(20, 'C', 'girls', 'Long Jump', 'field'),
(21, 'C', 'girls', 'Softball', 'field'),
(22, 'C', 'girls', '4x100', 'relay'),
(23, 'C', 'girls', '4x400', 'relay'),
(24, 'B', 'boys', '100m', 'racing'),
(25, 'B', 'boys', '200m', 'racing'),
(26, 'B', 'boys', '400m', 'racing'),
(27, 'B', 'boys', '800m', 'racing'),
(28, 'B', 'boys', '1500m', 'racing'),
(29, 'B', 'boys', 'High Jump', 'field'),
(30, 'B', 'boys', 'Javelin', 'field'),
(31, 'B', 'boys', 'Long Jump', 'field'),
(32, 'B', 'boys', 'Shot Put', 'field'),
(33, 'B', 'boys', '4x100', 'relay'),
(34, 'B', 'boys', '4x400', 'relay'),
(35, 'B', 'girls', '100m', 'racing'),
(36, 'B', 'girls', '200m', 'racing'),
(37, 'B', 'girls', '400m', 'racing'),
(38, 'B', 'girls', '800m', 'racing'),
(39, 'B', 'girls', '1500m', 'racing'),
(40, 'B', 'girls', 'High Jump', 'field'),
(41, 'B', 'girls', 'Javelin', 'field'),
(42, 'B', 'girls', 'Long Jump', 'field'),
(43, 'B', 'girls', 'Shot Put', 'field'),
(44, 'B', 'girls', 'Softball', 'field'),
(45, 'B', 'girls', '4x100', 'relay'),
(46, 'B', 'girls', '4x400', 'relay'),
(47, 'A', 'boys', '100m', 'racing'),
(48, 'A', 'boys', '200m', 'racing'),
(49, 'A', 'boys', '400m', 'racing'),
(50, 'A', 'boys', '800m', 'racing'),
(51, 'A', 'boys', '1500m', 'racing'),
(52, 'A', 'boys', 'High Jump', 'field'),
(53, 'A', 'boys', 'Javelin', 'field'),
(54, 'A', 'boys', 'Long Jump', 'field'),
(55, 'A', 'boys', 'Shot Put', 'field'),
(56, 'A', 'boys', '4x100', 'relay'),
(57, 'A', 'boys', '4x400', 'relay'),
(58, 'A', 'girls', '100m', 'racing'),
(59, 'A', 'girls', '200m', 'racing'),
(60, 'A', 'girls', '400m', 'racing'),
(61, 'A', 'girls', '800m', 'racing'),
(62, 'A', 'girls', '1500m', 'racing'),
(63, 'A', 'girls', 'High Jump', 'field'),
(64, 'A', 'girls', 'Javelin', 'field'),
(65, 'A', 'girls', 'Long Jump', 'field'),
(66, 'A', 'girls', '4x100', 'relay'),
(67, 'A', 'girls', '4x400', 'relay'),
(68, 'A', 'girls', 'Shot Put', 'field');

-- Insert additional stu_info data (total 10 athletes + 2 new for relay)
INSERT INTO stu_info (stu_id, name, class, clno, gender, dob, gmail, house) VALUES
(20201001, 'Chan Tai Man', '5C', 1, 'M', '2008-01-15', 's20201001@caremelss.edu.hk', 'Trust'),
(20201002, 'Lee Wai Shan', '5B', 2, 'F', '2008-02-20', 's20201002@caremelss.edu.hk', 'Intellect'),
(20211003, 'Wong Ho Yin', '4A', 3, 'M', '2009-03-10', 's20211003@caremelss.edu.hk', 'Loyalty'),
(20211004, 'Cheung Ka Yan', '4D', 4, 'F', '2009-04-05', 's20211004@caremelss.edu.hk', 'Virtue'),
(20221005, 'Lam King Sum', '3C', 5, 'M', '2010-05-12', 's20221005@caremelss.edu.hk', 'Trust'),
(20221006, 'Mak Ching Yi', '3B', 6, 'F', '2010-06-18', 's20221006@caremelss.edu.hk', 'Intellect'),
(20231007, 'Siu Man Kit', '2A', 7, 'M', '2011-07-22', 's20231007@caremelss.edu.hk', 'Loyalty'),
(20231008, 'Kwok Mei Mei', '2D', 8, 'F', '2011-08-01', 's20231008@caremelss.edu.hk', 'Virtue'),
(20241009, 'Tang Chun Kit', '1C', 9, 'M', '2012-09-09', 's20241009@caremelss.edu.hk', 'Trust'),
(20221010, 'Chow Ka Lok', '3A', 10, 'M', '2010-03-25', 's20221010@caremelss.edu.hk', 'Trust'), -- New student for relay
(20231011, 'Yeung Chi Ho', '2B', 11, 'M', '2011-04-15', 's20231011@caremelss.edu.hk', 'Trust'); -- New student for relay

INSERT INTO participants (stu_id, event_id, athlete_id) VALUES
(20221005, 1, '0001'), -- C boys 100m
(20221005, 7, '0001'), -- C boys High Jump
(20221005, 11, '0001'), -- C boys 4x100 relay (Trust)
(20231007, 7, '0002'), -- C boys High Jump
(20231007, 1, '0002'), -- C boys 100m
(20241009, 1, '0003'), -- C boys 100m
(20241009, 11, '0003'), -- C boys 4x100 relay (Trust)
(20221006, 13, '0004'), -- C girls 100m
(20231008, 13, '0005'), -- C girls 100m
(20201033, 47, '0006'), -- A boys 100m
(20201033, 56, '0006'), -- A boys 4x100 relay
(20201001, 47, '0007'), -- A boys 100m
(20201001, 56, '0007'),
(20201001, 54, '0007'), -- A boys Long Jump
(20211004, 35, '0008'), -- B girls 100m
(20211004, 42, '0008'), -- B girls Long Jump
(20201002, 58, '0009'), -- A girls 100m
(20211003, 24, '0010'), -- B boys 100m
(20221010, 11, '0011'), -- C boys 4x100 relay (Trust - new)
(20231011, 11, '0012'); -- C boys 4x100 relay (Trust - new)


-- Insert racing_result data
INSERT INTO racing_result (event_id, types, athlete_id, time) VALUES
(1, 'final', '0001', 13.5), -- C boys 100m
(1, 'final', '0002', 14.1),
(1, 'final', '0003', 13.8),
(13, 'final', '0004', 15.2), -- C girls 100m
(13, 'final', '0005', 14.9),
(47, 'final', '0006', 11.8), -- A boys 100m
(47, 'final', '0007', 12.0),
(58, 'final', '0009', 13.5), -- A girls 100m
(24, 'final', '0010', 12.5), -- B boys 100m
(35, 'final', '0008', 14.0); -- B girls 100m

-- Insert field_result data
INSERT INTO field_result (event_id, types, athlete_id, trial, distance) VALUES
(7, 'final', '0001', 1, 1.60), -- C boys High Jump
(7, 'final', '0002', 1, 1.55),
(54, 'final', '0007', 1, 6.20), -- A boys Long Jump
(42, 'final', '0008', 1, 4.80); -- B girls Long Jump

INSERT INTO relay_result (event_id, types, athlete_id, position, team, time) VALUES
(11, 'individual', '0001', 1, 'Trust', 13.0), -- C boys 4x100, individual leg 1
(11, 'individual', '0003', 2, 'Trust', 14.2), -- C boys 4x100, individual leg 2
(11, 'individual', '0011', 3, 'Trust', 13.5), -- C boys 4x100, individual leg 3
(11, 'individual', '0012', 4, 'Trust', 12.8); -- C boys 4x100, individual leg 4

