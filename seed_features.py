import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'student_management.settings'
django.setup()

from clubs.models import Club, ClubMembership, ClubEvent
from notices.models import Notice
from events.models import Event
from fees.models import FeeStructure
from library.models import Book
from placements.models import Company, PlacementDrive
from hostel.models import Hostel, Room
from accounts.models import User
from django.utils import timezone
from datetime import date, timedelta, datetime

today = timezone.localdate()

# ── Clubs ──
if Club.objects.count() == 0:
    print("Seeding Clubs...")
    c1 = Club.objects.create(name='Drama Club', description='A platform for students to showcase their acting, directing, and stage management talents. Regular theatre workshops and annual stage productions.', category='Cultural', coordinator=None)
    c2 = Club.objects.create(name='Music Club', description='For music enthusiasts — vocal, instrumental, and choir. Regular jam sessions, open mics, and inter-college music competitions.', category='Cultural')
    c3 = Club.objects.create(name='Debate Society', description='Hone your public speaking and critical thinking skills. Participate in debates, extempore, group discussions, and parliamentary debates.', category='Academic')
    c4 = Club.objects.create(name='Photography Club', description='Explore the art of photography and videography. Workshops on composition, editing, and annual photography exhibitions.', category='Cultural')
    c5 = Club.objects.create(name='Robotics Club', description='Build and program robots. Participate in Robocon, line followers, drone challenges, and inter-college robotics competitions.', category='Technical')
    c6 = Club.objects.create(name='Coding Club', description='Competitive programming, hackathons, open-source contributions, and coding bootcamps. For aspiring software developers.', category='Technical')
    c7 = Club.objects.create(name='Sports Club', description='Promotes sports and fitness among students. Organizes intra-college tournaments in cricket, football, basketball, and athletics.', category='Sports')
    c8 = Club.objects.create(name='Literary Club', description='Creative writing, poetry, storytelling, and book reviews. Annual literary magazine publication.', category='Academic')
    c9 = Club.objects.create(name='Dance Club', description='Learn and perform various dance forms — classical, contemporary, hip-hop, and folk. Annual dance fest participation.', category='Cultural')
    c10 = Club.objects.create(name='Entrepreneurship Cell', description='Fosters startup culture. Business plan competitions, speaker sessions, mentorship programs, and incubation support.', category='Technical')

    for c in [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]:
        ClubEvent.objects.create(club=c, title=f'{c.name} Meetup', description=f'First meetup for {c.name}', date=timezone.now() + timedelta(days=15), venue='Seminar Hall')

    print(f"  Created {Club.objects.count()} clubs")

# ── Notices ──
if Notice.objects.count() == 0:
    print("Seeding Notices...")
    admin = User.objects.filter(is_superuser=True).first()
    notices_data = [
        ('Even Semester Exam Schedule Released', 'The even semester examination schedule has been released. Students can download their admit cards from the result portal. Examinations will commence from 15th July 2026.', 'exam'),
        ('College Foundation Day Celebration', 'The 24th Foundation Day of the institute will be celebrated on 12th August 2026. All students and staff are expected to attend the ceremony.', 'event'),
        ('Summer Vacation Notice', 'The institute will remain closed for summer vacation from 1st June to 30th June 2026. Regular classes will resume from 1st July 2026.', 'holiday'),
        ('Industry Visit for CSE Students', 'An industry visit to Tech Mahindra has been arranged for CSE final year students on 20th July 2026. Interested students may register with the department.', 'academic'),
        ('Scholarship Application Open', 'Applications are invited for the Swami Vivekananda Scholarship for the academic year 2026-27. Last date to apply is 31st August 2026.', 'general'),
        ('Placement Drive Notice', 'TCS, Infosys, and Wipro will be visiting campus for placements in August 2026. Eligible students should register on the placement portal.', 'placement'),
        ('Library Timings Extended', 'The library will remain open from 7:00 AM to 10:00 PM during examination days. All sections will be operational.', 'academic'),
        ('Sports Meet 2026', 'The annual inter-department sports meet will be held from 5th to 10th September 2026. Register your teams with the Sports Club.', 'event'),
        ('Hostel Room Allocation', 'Hostel room allocation for the new academic session will begin from 20th July 2026. Students must complete the online registration.', 'general'),
        ('Faculty Development Program', 'A week-long FDP on "AI in Engineering Education" will be conducted from 22nd to 28th July 2026. Faculty members are encouraged to register.', 'academic'),
    ]
    for title, content, cat in notices_data:
        Notice.objects.create(title=title, content=content, category=cat, posted_by=admin)
    print(f"  Created {Notice.objects.count()} notices")

# ── Events ──
if Event.objects.count() == 0:
    print("Seeding Events...")
    events_data = [
        ('Tech Fest 2026', 'Annual technical festival with robotics, coding, paper presentations, and workshops.', datetime(2026, 9, 15, 9, 0), datetime(2026, 9, 17, 17, 0), 'Main Auditorium', 'technical'),
        ('Cultural Fest - Mirage 2026', 'Three-day cultural extravaganza featuring dance, music, drama, and fashion show.', datetime(2026, 10, 20, 10, 0), datetime(2026, 10, 22, 22, 0), 'College Ground', 'cultural'),
        ('Annual Sports Day', 'Inter-department athletics, team sports, and prize distribution ceremony.', datetime(2026, 11, 10, 7, 0), None, 'Sports Complex', 'sports'),
        ('AI Workshop', 'Hands-on workshop on Machine Learning and Deep Learning using Python.', datetime(2026, 8, 5, 14, 0), datetime(2026, 8, 5, 17, 0), 'Computer Lab 3', 'workshop'),
        ('Guest Lecture: Career in Data Science', 'Industry expert from Google shares insights on building a career in data science.', datetime(2026, 7, 25, 11, 0), None, 'Seminar Hall', 'seminar'),
        ('Hackathon 2026', '24-hour coding hackathon. Build innovative solutions for real-world problems. Prizes worth ₹50,000.', datetime(2026, 9, 8, 9, 0), datetime(2026, 9, 9, 9, 0), 'Innovation Lab', 'technical'),
        ('Entrepreneurship Summit', 'Meet successful entrepreneurs, pitch your ideas, and network with investors.', datetime(2026, 11, 5, 10, 0), datetime(2026, 11, 6, 17, 0), 'Conference Hall', 'seminar'),
        ('Freshers Party 2026', 'Welcome party for the new batch. Cultural performances, games, and fun activities.', datetime(2026, 8, 30, 18, 0), None, 'College Auditorium', 'cultural'),
    ]
    now_aware = timezone.now()
    for title, desc, start, end, venue, cat in events_data:
        start_aware = timezone.make_aware(start)
        end_aware = timezone.make_aware(end) if end else None
        Event.objects.create(title=title, description=desc, date=start_aware, end_date=end_aware, venue=venue, category=cat, is_upcoming=(start_aware > now_aware))
    print(f"  Created {Event.objects.count()} events")

# ── Fee Structure ──
if FeeStructure.objects.count() == 0:
    print("Seeding Fee Structure...")
    fees_data = [
        ('Tuition Fee', 45000, 'Sem 1-4'), ('Tuition Fee', 48000, 'Sem 5-8'),
        ('Development Fee', 8000, 'Sem 1-8'), ('Library Fee', 3000, 'Sem 1-8'),
        ('Laboratory Fee', 5000, 'Sem 1-6'), ('Sports Fee', 2000, 'Sem 1-8'),
        ('Hostel Fee', 35000, 'Sem 1-8'), ('Transport Fee', 12000, 'Sem 1-8'),
        ('Examination Fee', 2500, 'Sem 1-8'), ('Medical Insurance', 1500, 'Sem 1-8'),
        ('Student Welfare Fund', 1000, 'Sem 1-8'), ('Alumni Fee', 500, 'Sem 1-8'),
    ]
    for name, amt, sem in fees_data:
        FeeStructure.objects.create(name=name, amount=amt, due_date=date(2026, 7, 15), semester=sem)
    print(f"  Created {FeeStructure.objects.count()} fee items")

# ── Books ──
if Book.objects.count() == 0:
    print("Seeding Books...")
    books_data = [
        ('Introduction to Algorithms', 'Thomas H. Cormen', '978-0262033848', 10, 7, 'A1'),
        ('Computer Networks', 'Andrew S. Tanenbaum', '978-0132126953', 8, 5, 'A2'),
        ('Operating System Concepts', 'Abraham Silberschatz', '978-1118063330', 6, 3, 'A3'),
        ('Database Management Systems', 'Raghu Ramakrishnan', '978-0072465631', 5, 4, 'B1'),
        ('Artificial Intelligence: A Modern Approach', 'Stuart Russell', '978-0136042594', 4, 2, 'B2'),
        ('Engineering Mathematics', 'B.S. Grewal', '978-8174092038', 15, 12, 'C1'),
        ('Theory of Machines', 'S.S. Rattan', '978-1259001705', 6, 5, 'C2'),
        ('Heat and Mass Transfer', 'R.K. Rajput', '978-8131807963', 7, 4, 'C3'),
        ('Digital Electronics', 'M. Morris Mano', '978-0131988503', 8, 6, 'D1'),
        ('Microprocessor Architecture', 'Ramesh S. Gaonkar', '978-1891129205', 5, 3, 'D2'),
        ('Control Systems Engineering', 'Nise', '978-1118170519', 4, 2, 'D3'),
        ('Fluid Mechanics', 'Cengel & Cimbala', '978-0073380322', 6, 3, 'E1'),
        ('Strength of Materials', 'R.K. Bansal', '978-8131808144', 9, 7, 'E2'),
        ('Environmental Engineering', 'Peavy & Rowe', '978-0070491342', 3, 2, 'E3'),
        ('Python Programming', 'John Zelle', '978-1590282410', 7, 5, 'F1'),
        ('Data Science from Scratch', 'Joel Grus', '978-1492041139', 4, 3, 'F2'),
        ('Clean Code', 'Robert C. Martin', '978-0132350884', 5, 4, 'F3'),
        ('The C Programming Language', 'Kernighan & Ritchie', '978-0131103627', 10, 6, 'G1'),
        ('Object Oriented Programming with C++', 'E. Balagurusamy', '978-1259029938', 8, 5, 'G2'),
        ('Software Engineering', 'Pressman', '978-0073375977', 6, 4, 'G3'),
    ]
    for title, author, isbn, total, avail, rack in books_data:
        Book.objects.create(title=title, author=author, isbn=isbn, total_copies=total, available_copies=avail, rack_number=rack)
    print(f"  Created {Book.objects.count()} books")

# ── Companies ──
if Company.objects.count() == 0:
    print("Seeding Placement Partners...")
    companies_data = [
        ('TCS', 'Tata Consultancy Services — a global leader in IT services, consulting & business solutions.', 'https://www.tcs.com', 12),
        ('Infosys', 'Global leader in next-generation digital services and consulting.', 'https://www.infosys.com', 11),
        ('Wipro', 'Leading global information technology, consulting and business process services company.', 'https://www.wipro.com', 10),
        ('Accenture', 'Global professional services company with leading capabilities in digital, cloud and security.', 'https://www.accenture.com', 13),
        ('Microsoft', 'Empowering every person and every organization on the planet to achieve more.', 'https://www.microsoft.com', 25),
        ('Google', 'American multinational technology company specializing in Internet-related services.', 'https://www.google.com', 28),
        ('Amazon', 'Focuses on e-commerce, cloud computing, digital streaming, and artificial intelligence.', 'https://www.amazon.com', 22),
        ('Flipkart', 'Indian e-commerce company headquartered in Bangalore, offering a wide range of products.', 'https://www.flipkart.com', 14),
        ('Adobe', 'American multinational computer software company known for its creative and multimedia software.', 'https://www.adobe.com', 18),
        ('Mahindra & Mahindra', 'Indian multinational automotive manufacturing company.', 'https://www.mahindra.com', 8),
        ('Larsen & Toubro', 'Indian multinational conglomerate in engineering, construction, and technology.', 'https://www.lnt.com', 9),
        ('HCL Technologies', 'Indian multinational IT services and consulting company.', 'https://www.hcltech.com', 10),
    ]
    for name, desc, url, pkg in companies_data:
        Company.objects.create(name=name, description=desc, website=url, avg_package=pkg)
    print(f"  Created {Company.objects.count()} companies")

    # Placement drives
    companies = list(Company.objects.all())
    for i, company in enumerate(companies[:6]):
        PlacementDrive.objects.create(
            company=company,
            title=f'{company.name} Campus Recruitment 2026',
            description=f'{company.name} is hiring final year students for various roles. This is an excellent opportunity to start your career with a leading organization.',
            application_deadline=date(2026, 8, 15) + timedelta(days=i * 7),
            drive_date=date(2026, 9, 1) + timedelta(days=i * 7),
            eligibility_criteria='B.Tech all branches, CGPA 6.0+, no active backlogs',
            is_active=True,
        )
    print(f"  Created {PlacementDrive.objects.count()} drives")

# ── Hostels ──
if Hostel.objects.count() == 0:
    print("Seeding Hostels...")
    h1 = Hostel.objects.create(name='Boys Hostel - A', gender='male', warden='Dr. Ramesh Singh', contact='0512-2550101', address='Main Campus, North Block', total_rooms=50)
    h2 = Hostel.objects.create(name='Boys Hostel - B', gender='male', warden='Mr. Suresh Yadav', contact='0512-2550102', address='Main Campus, East Block', total_rooms=40)
    h3 = Hostel.objects.create(name='Girls Hostel', gender='female', warden='Dr. Neha Sharma', contact='0512-2550103', address='Main Campus, South Block', total_rooms=35)
    h4 = Hostel.objects.create(name='International Hostel', gender='coed', warden='Prof. Alok Verma', contact='0512-2550104', address='Main Campus, West Wing', total_rooms=20)

    room_data = [
        (h1, ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110'], 3),
        (h1, ['201', '202', '203', '204', '205', '206', '207', '208', '209', '210'], 2),
        (h2, ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10'], 2),
        (h2, ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10'], 3),
        (h3, ['G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10'], 2),
        (h3, ['G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20'], 3),
        (h4, ['I01', 'I02', 'I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09', 'I10'], 1),
    ]
    for hostel, rooms, cap in room_data:
        for rnum in rooms:
            Room.objects.create(hostel=hostel, room_number=rnum, capacity=cap, occupied=0, rent_per_month=3000 if cap == 3 else (4000 if cap == 2 else 6000))
    print(f"  Created {Room.objects.count()} rooms across {Hostel.objects.count()} hostels")

print("\nAll feature data seeded successfully!")
